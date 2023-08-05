import asyncio
import logging
import signal
from copy import copy
from dataclasses import dataclass
from typing import List, Callable, Coroutine, Mapping, Optional, Any

from aio_pika.patterns import RPC

from kode_rpc import request_trace_id
from kode_rpc.method import RPCMethod
from kode_rpc.rabbitmq import RabbitMQ
from kode_rpc.util.rpc import JsonRPC

logger = logging.getLogger(__name__)


@dataclass
class RPCRequestInfo:
    trace_id: str
    master: str
    payload: Mapping


MethodExceptionHandler = Callable[[RPCMethod, BaseException, RPCRequestInfo], Coroutine[Any, Any, Mapping]]
MethodLogger = Callable[[RPCMethod, Mapping, RPCRequestInfo], Coroutine]


class RPCServer:
    def __init__(self, application_name: str, *, rabbitmq_host: str, rabbitmq_user: str, rabbitmq_password: str):
        self._application_name = application_name
        self._broker = RabbitMQ(
            host=rabbitmq_host,
            user=rabbitmq_user,
            password=rabbitmq_password,
        )
        self._methods: List[RPCMethod] = []
        self._method_logger: Optional[MethodLogger] = None
        self._method_exception_handler: Optional[MethodExceptionHandler] = None
        self._rpc: Optional[RPC] = None
        self._shutdown_future = asyncio.get_event_loop().create_future()

    def method_logger(self, func: MethodLogger):
        self._method_logger = func

    def method_exception_handler(self, func: MethodExceptionHandler):
        self._method_exception_handler = func

    async def register_methods(self, methods: List[RPCMethod]):
        self._methods = methods

        await self._broker.connect()
        assert self._broker.connection, 'Broker connection is broken'

        try:
            channel = await self._broker.connection.channel()
            self._rpc = await JsonRPC.create(channel)

            await asyncio.gather(*(
                self._rpc.register(
                    self._get_method_full_name(method),
                    self._method_wrapper(method),
                    auto_delete=True
                ) for method in self._methods
            ))
        except BaseException:
            await self._broker.disconnect()
            raise

    async def serve(self):
        logger.info('Awaiting RPC requests')
        loop = asyncio.get_event_loop()

        for s in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(s, lambda s=s: asyncio.create_task(self._shutdown(s)))

        await self._shutdown_future

    async def _shutdown(self, received_signal: signal.Signals):
        logger.info(f'Shutting down RPC server due to [{received_signal.name}]')
        try:
            if self._rpc:
                await self._rpc.close()
        finally:
            await self._broker.disconnect()
            self._shutdown_future.set_result(None)
        logger.info('RPC server successfully terminated')

    def _get_method_full_name(self, method: RPCMethod) -> str:
        return f'{self._application_name}_{method.name}_v{method.version}'

    def _method_wrapper(self, method: RPCMethod):
        async def wrapper(*args, **kwargs):
            arguments = copy(kwargs)
            trace_id = arguments.pop('trace_id')
            master = arguments.pop('master')

            request_info = RPCRequestInfo(payload=arguments, trace_id=trace_id, master=master)
            request_trace_id.set(request_info.trace_id)

            try:
                result = await method(**arguments)
            except BaseException as exc:
                if not self._method_exception_handler:
                    raise

                result = await self._method_exception_handler(method, exc, request_info)

            if self._method_logger:
                await self._method_logger(method, result, request_info)

            return result

        return wrapper
