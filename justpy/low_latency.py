__all__ = ['logger_config', 'set_logger_config', 'log', 'set_logger', 'scheduler', 'set_scheduler', 'thread_pool_executor', 'set_thread_pool_executor']

from async_generator import asynccontextmanager, async_generator, yield_
from enum import Enum
import logging
import asyncio
from typing import Optional, Callable, AsyncContextManager
from functools import partial


def _default_logger_config(*args, **kwargs):
    logging.basicConfig(*args, **kwargs)


_logger_config = _default_logger_config


def set_logger_config(callable: Callable):
    global _logger_config
    _logger_config = callable


def logger_config() -> Callable:
    return _logger_config


async def _default_logger(log_level, *args, **kwargs):
    if logging.CRITICAL == log_level:
        logging.critical(*args, **kwargs)
    elif logging.FATAL == log_level:
        logging.critical(*args, **kwargs)
    elif logging.ERROR == log_level:
        logging.error(*args, **kwargs)
    elif logging.WARNING == log_level:
        logging.warning(*args, **kwargs)
    elif logging.WARN == log_level:
        logging.warn(*args, **kwargs)
    elif logging.INFO == log_level:
        logging.info(*args, **kwargs)
    elif logging.DEBUG == log_level:
        logging.debug(*args, **kwargs)
    elif logging.NOTSET == log_level:
        pass


_log = _default_logger


def set_logger(async_callable: Callable):
    global _log
    _log = async_callable


def log() -> Callable:
    return _log


class _BasicYield:
    async def __call__(self):
        await asyncio.sleep(0)


@asynccontextmanager
@async_generator
async def _default_scheduler():
    await yield_(_BasicYield())  # can not determine coro scheduler loop


_scheduler = _default_scheduler


def set_scheduler(async_context_manager: AsyncContextManager):
    global _scheduler
    _scheduler = async_context_manager


def scheduler() -> AsyncContextManager:
    return _scheduler


async def _default_thread_pool_executor(loop: Optional[asyncio.AbstractEventLoop], worker: Callable, *args, **kwargs):
    loop = loop or asyncio.get_event_loop()
    worker_with_args = partial(worker, *args, **kwargs)
    return await loop.run_in_executor(None, worker_with_args)


_thread_pool_executor = _default_thread_pool_executor


def set_thread_pool_executor(async_callable: Callable):
    global _thread_pool_executor
    _thread_pool_executor = async_callable


def thread_pool_executor() -> Callable:
    return _thread_pool_executor
