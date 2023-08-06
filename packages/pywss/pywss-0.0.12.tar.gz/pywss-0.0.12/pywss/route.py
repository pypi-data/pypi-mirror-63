import functools

from importlib import import_module
from pywss.public import InvalidPath


def route(path):
    def wrapper(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        _wrapper.__route__ = path
        return _wrapper

    return wrapper


class Route:
    routes = {}  # all routes for server
    finish = []  # this will work in SocketHandler.finish

    @classmethod
    def add_routes(cls, module_name):
        point = module_name.rfind('.')
        if point == (-1):
            mod = import_module(module_name)
        else:
            mod = getattr(import_module(module_name[:point]), module_name[point + 1:])
        for attr in dir(mod):
            if attr.startswith('_'):
                continue
            func = getattr(mod, attr)
            path = getattr(func, '__route__', None)
            if path and callable(func):
                cls.add_route(path, func)

    @classmethod
    def add_route(cls, path, func):
        cls.routes.setdefault(path, func)

    @classmethod
    def add_finish(cls, func):
        cls.finish.append(func)

    @classmethod
    def get(cls, path):
        func = cls.routes.get(path)
        if not func:
            raise InvalidPath
        return func
