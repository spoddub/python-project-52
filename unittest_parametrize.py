from functools import wraps
from unittest import TestCase


def _iter_params(param_list):
    for p in param_list:
        if isinstance(p, dict):
            yield (), p
        elif isinstance(p, (list, tuple)):
            yield tuple(p), {}
        else:
            yield (p,), {}


def parametrize(params):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for args_i, kwargs_i in _iter_params(params):
                with self.subTest(**kwargs_i):
                    func(self, *args_i, **kwargs_i)

        return wrapper

    return decorator


class ParametrizedTestCase(TestCase):
    pass
