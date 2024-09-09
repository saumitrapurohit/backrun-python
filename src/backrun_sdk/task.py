import functools
import inspect
import logging

from .api import get_active_client

logger = logging.getLogger("backrun")


def task(_func=None, *, cron=None):
    def decorator(func):
        module_name = inspect.getmodule(func).__name__
        name = f"{module_name}.{func.__name__}"

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                logger.error("task.failed: %s", str(exc))

        def delay(*args, **kwargs):
            client = get_active_client()

            if not client:
                logger.error("backrun client not found, executing directly")
                return func(*args, **kwargs)

            if client.always_eager:
                return func(*args, **kwargs)

            client.submit(name, args, kwargs)

        def apply_async(args=None, kwargs=None, countdown=None):
            args = args or []
            kwargs = kwargs or {}
            return delay(*args, **kwargs)

        wrapper.delay = delay
        wrapper.apply_async = apply_async
        wrapper.is_backrun_task = True
        wrapper.name = name
        wrapper.cron = cron

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


__all__ = ["task"]
