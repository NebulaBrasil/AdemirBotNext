import asyncio
import functools


def async_test(func):
    """Decorator to turn an async function into a test case."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        coro = func(*args, **kwargs)
        loop.run_until_complete(coro)
    return wrapper