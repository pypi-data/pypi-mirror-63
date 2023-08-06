import abc
import logging
import functools as ft
import json
from types import SimpleNamespace

from pjrpc import common
from pjrpc.common import generators, exceptions, v20

logger = logging.getLogger(__package__)


class Batch:
    """
    Batch wrapper. Implements some methods to wrap multiple JSON-RPC requests into a single batch request.

    :param client: JSON-RPC client instance
    :param strict: if ``True`` checks that all requests have theirs corresponding responses
    """

    class Proxy:
        """
        Proxy object. Provides syntactic sugar to make method calls using dot notation.

        :param batch: batch wrapper
        """

        def __init__(self, batch):
            self._batch = batch

        def __getattr__(self, attr):
            def wrapped(*args, **kwargs):
                self._batch.add(attr, *args, **kwargs)
                return self

            return wrapped

        def __call__(self, _trace_ctx=SimpleNamespace()):
            """
            Makes an RPC call.

            :param _trace_ctx: tracers request context
            """

            return self.call(_trace_ctx)

        def call(self, _trace_ctx=SimpleNamespace()):
            """
            Makes an RPC call.

            :param _trace_ctx: tracers request context
            """

            return self._batch.call(_trace_ctx)

    @property
    def proxy(self):
        """
        Batch request proxy object.
        """

        return Batch.Proxy(self)

    def __init__(self, client):
        self._client = client
        self._error_cls = client.error_cls
        self._id_gen = client.id_gen()
        self._requests = client.batch_request_class()

    def __getitem__(self, requests):
        """
        Adds requests to the batch and makes a request.

        :param requests: requests to be added to the batch
        :returns: request results as a tuple
        """

        self._requests.extend([
            self._client.request_class(
                method=method,
                params=params,
                id=next(self._id_gen),
            ) for method, *params in requests
        ])
        return self.call()

    def __call__(self, method, *args, **kwargs):
        """
        Adds the method call to the batch.

        :param method: method name
        :param args: method positional arguments
        :param kwargs: method named arguments
        :returns: self
        """

        return self.add(method, *args, **kwargs)

    def add(self, method, *args, **kwargs):
        """
        Adds the method call to the batch.

        :param method: method name
        :param args: method positional arguments
        :param kwargs: method named arguments
        :returns: self
        """

        assert not (args and kwargs), "positional and keyword arguments are mutually exclusive"

        self._requests.append(self._client.request_class(method, args or kwargs, id=next(self._id_gen)))
        return self

    def call(self, _trace_ctx=SimpleNamespace()):
        """
        Makes a JSON-RPC request.

        :param _trace_ctx: tracers request context
        :returns: request results as a tuple
        """

        response = self.send(self._requests)

        return response.result if response is not None else None

    def send(self, request, _trace_ctx=SimpleNamespace(), **kwargs):
        """
        Sends a JSON-RPC batch request.

        :param request: request instance
        :param kwargs: additional client request argument
        :param _trace_ctx: tracers request context
        :returns: response instance
        """

        kwargs = {**self._client._request_args, **kwargs}

        request_text = self._client.json_dumper(request, cls=self._client.json_encoder)
        for tracer in self._client._tracers:
            tracer.on_batch_begin(_trace_ctx, request)

        try:
            response_text = self._client._request(request_text, request.is_notification, **kwargs)
            if not request.is_notification:
                response = self._client.batch_response_class.from_json(
                    self._client.json_loader(response_text, cls=self._client.json_decoder),
                    error_cls=self._client.error_cls,
                )
                if response.is_success:
                    self._relate(request, response)
            else:
                response = None

        except BaseException as e:
            for tracer in self._client._tracers:
                tracer.on_error(_trace_ctx, request, e)
            raise

        for tracer in self._client._tracers:
            tracer.on_batch_end(_trace_ctx, request, response)

        return response

    def notify(self, method, *args, **kwargs):
        """
        Adds a notification request to the batch.

        :param method: method name
        :param args: method positional arguments
        :param kwargs: method named arguments
        """

        assert not (args and kwargs), "positional and keyword arguments are mutually exclusive"

        self._requests.append(self._client.request_class(method, args or kwargs))
        return self

    def _relate(self, batch_request, batch_response):
        """
        Sets requests `related` field. if `strict` flag is ``True``
        checks that all requests have theirs corresponding responses

        :param batch_request: batch request
        :param batch_response: batch response
        """

        response_map = {response.id: response for response in batch_response if response.id is not None}

        for request in batch_request:
            if request.id is not None:
                related = response_map.pop(request.id, None)
                if related is None and self._client._strict:
                    raise exceptions.IdentityError(f"response '{request.id}' not found")
                else:
                    request.related = related

        if response_map and self._client._strict:
            raise exceptions.IdentityError(f"unexpected response found: {response_map.keys()}")


class AsyncBatch(Batch):
    """
    Asynchronous batch wrapper. Used to make asynchronous JSON-RPC batch requests.
    """

    async def call(self, _trace_ctx=SimpleNamespace()):
        """
        Makes a JSON-RPC request.

        :param _trace_ctx: tracers request context
        :returns: request results as a tuple
        """

        response = await self.send(self._requests, _trace_ctx=_trace_ctx)

        return response.result if response is not None else None

    async def send(self, request, _trace_ctx=SimpleNamespace(), **kwargs):
        """
        Sends a JSON-RPC batch request.

        :param request: request instance
        :param kwargs: additional client request argument
        :param _trace_ctx: tracers request context
        :returns: response instance
        """

        kwargs = {**self._client._request_args, **kwargs}

        request_text = self._client.json_dumper(request, cls=self._client.json_encoder)
        for tracer in self._client._tracers:
            tracer.on_batch_begin(_trace_ctx, request)

        try:
            response_text = await self._client._request(request_text, request.is_notification, **kwargs)
            if not request.is_notification:
                response = self._client.batch_response_class.from_json(
                    self._client.json_loader(response_text, cls=self._client.json_decoder),
                    error_cls=self._client.error_cls,
                )
                if response.is_success:
                    self._relate(request, response)
            else:
                response = None

        except BaseException as e:
            for tracer in self._client._tracers:
                tracer.on_error(_trace_ctx, request, e)
            raise

        for tracer in self._client._tracers:
            tracer.on_batch_end(_trace_ctx, request, response)

        return response


class AbstractClient(abc.ABC):
    """
    Abstract JSON-RPC client.

    :param request_class: request class
    :param response_class: response class
    :param batch_request_class: batch request class
    :param batch_response_class: batch response class
    :param id_gen: identifier generator
    :param json_loader: json loader
    :param json_dumper: json dumper
    :param json_encoder: json encoder
    :param json_decoder: json decoder
    :param error_cls: JSON-RPC error base class
    :param strict: if ``True`` checks that a request and a response identifiers match
    """

    class Proxy:
        """
        Proxy object. Provides syntactic sugar to make method call using dot notation.

        :param client: JSON-RPC client instance
        """

        def __init__(self, client):
            self._client = client

        def __getattr__(self, attr):
            return ft.partial(self._client.call, attr)

    @property
    def proxy(self):
        """
        Clint proxy object.
        """

        return AbstractClient.Proxy(self)

    @property
    def batch(self):
        """
        Client batch wrapper.
        """

        return Batch(self)

    @abc.abstractmethod
    def _request(self, request_text, is_notification=False, **kwargs):
        """
        Makes a JSON-RPC request.

        :param request_text: request text representation
        :param is_notification: is the request a notification
        :returns: response text representation
        """

    def __init__(
        self,
        request_class=v20.Request,
        response_class=v20.Response,
        batch_request_class=v20.BatchRequest,
        batch_response_class=v20.BatchResponse,
        error_cls=exceptions.JsonRpcError,
        id_gen=generators.sequential,
        json_loader=json.loads,
        json_dumper=json.dumps,
        json_encoder=common.JSONEncoder,
        json_decoder=None,
        strict=True,
        request_args=None,
        tracers=(),
    ):
        self.request_class = request_class
        self.response_class = response_class
        self.batch_request_class = batch_request_class
        self.batch_response_class = batch_response_class
        self.error_cls = error_cls
        self.json_loader = json_loader
        self.json_dumper = json_dumper
        self.json_encoder = json_encoder
        self.json_decoder = json_decoder
        self.id_gen = id_gen
        self._strict = strict
        self._request_args = request_args or {}
        self._tracers = tracers

    def __call__(self, method, *args, _trace_ctx=SimpleNamespace(), **kwargs):
        """
        Makes JSON-RPC call.

        :param method: method name
        :param args: method positional arguments
        :param kwargs: method named arguments
        :param _trace_ctx: tracers request context
        :returns: response result
        """

        return self.call(method, *args, **kwargs)

    def send(self, request, _trace_ctx=SimpleNamespace(), **kwargs):
        """
        Sends a JSON-RPC request.

        :param request: request instance
        :param kwargs: additional client request argument
        :param _trace_ctx: tracers request context
        :returns: response instance
        """

        kwargs = {**self._request_args, **kwargs}

        request_text = self.json_dumper(request, cls=self.json_encoder)
        for tracer in self._tracers:
            tracer.on_request_begin(_trace_ctx, request)

        try:
            response_text = self._request(request_text, request.is_notification, **kwargs)
            if not request.is_notification:
                response = self.response_class.from_json(
                    self.json_loader(response_text, cls=self.json_decoder), error_cls=self.error_cls,
                )
                self._relate(request, response)
            else:
                if self._strict and response_text:
                    raise exceptions.BaseError("unexpected response")
                response = None

        except BaseException as e:
            for tracer in self._tracers:
                tracer.on_error(_trace_ctx, request, e)
            raise

        for tracer in self._tracers:
            tracer.on_request_end(_trace_ctx, request, response)

        return response

    def notify(self, method, *args, _trace_ctx=SimpleNamespace(), **kwargs):
        """
        Makes a notification request

        :param method: method name
        :param args: method positional arguments
        :param kwargs: method named arguments
        :param _trace_ctx: tracers request context
        """

        assert not (args and kwargs), "positional and keyword arguments are mutually exclusive"

        request = self.request_class(
            id=None,
            method=method,
            params=args or kwargs,
        )
        return self.send(request, _trace_ctx=_trace_ctx)

    def call(self, method, *args, _trace_ctx=SimpleNamespace(), **kwargs):
        """
        Makes JSON-RPC call.

        :param method: method name
        :param args: method positional arguments
        :param kwargs: method named arguments
        :param _trace_ctx: tracers request context
        :returns: response result
        """

        assert not (args and kwargs), "positional and keyword arguments are mutually exclusive"

        request = self.request_class(
            id=next(self.id_gen()),
            method=method,
            params=args or kwargs,
        )
        response = self.send(request, _trace_ctx=_trace_ctx)

        return response.result

    def _relate(self, request, response):
        """
        Checks the the request and the response identifiers match.

        :param request: request
        :param response: response
        """

        if self._strict and response.id != request.id:
            raise exceptions.IdentityError(
                f"response id doesn't match the request one: expected {request.id}, got {response.id}",
            )

        response.related = request


class AbstractAsyncClient(AbstractClient):
    """
    Abstract asynchronous JSON-RPC client.
    """

    @property
    def batch(self):
        """
        Client batch wrapper.
        """

        return AsyncBatch(self)

    @abc.abstractmethod
    async def _request(self, request_text, is_notification=False, **kwargs):
        """
        Makes a JSON-RPC request.

        :param request_text: request text representation
        :param is_notification: is the request a notification
        :returns: response text representation
        """

    async def send(self, request, _trace_ctx=SimpleNamespace(), **kwargs):
        """
        Sends a JSON-RPC request.

        :param request: request instance
        :param kwargs: additional client request argument
        :param _trace_ctx: tracers request context
        :returns: response instance
        """

        kwargs = {**self._request_args, **kwargs}

        request_text = self.json_dumper(request, cls=self.json_encoder)
        for tracer in self._tracers:
            tracer.on_request_begin(_trace_ctx, request)

        try:
            response_text = await self._request(request_text, request.is_notification, **kwargs)
            if not request.is_notification:
                response = self.response_class.from_json(
                    self.json_loader(response_text, cls=self.json_decoder), error_cls=self.error_cls,
                )
                self._relate(request, response)
            else:
                if self._strict and response_text:
                    raise exceptions.BaseError("unexpected response")
                response = None

        except BaseException as e:
            for tracer in self._tracers:
                tracer.on_error(_trace_ctx, request, e)
            raise

        for tracer in self._tracers:
            tracer.on_request_end(_trace_ctx, request, response)

        return response

    async def call(self, method, *args, _trace_ctx=SimpleNamespace(), **kwargs):
        """
        Makes JSON-RPC call.

        :param method: method name
        :param args: method positional arguments
        :param kwargs: method named arguments
        :param _trace_ctx: tracers request context
        :returns: response result
        """

        assert not (args and kwargs), "positional and keyword arguments are mutually exclusive"

        request = self.request_class(
            id=next(self.id_gen()),
            method=method,
            params=args or kwargs,
        )
        response = await self.send(request, _trace_ctx=_trace_ctx)

        return response.result
