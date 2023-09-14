import time
from functools import wraps
from itertools import count

import common.logger as logger

__all__ = ('backoff',)


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """Функция для повторного выполнения функции при ошибке."""

    def func_wrapper(func):
        _logger = logger.get_logger('backoff')

        @wraps(func)
        def inner(*args, **kwargs):
            for n in count(1, 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    t = min(start_sleep_time * (factor ^ n), border_sleep_time)

                    _logger.error(f'Error on func {func.__name__}: {e}. Making backoff. Repeat={n}', exc_info=True)
                    time.sleep(t)

        return inner

    return func_wrapper
