import inspect
from time import time


class AppRoute:
    routes = dict()

    def __init__(self, url):
        self.url = url

    def __call__(self, cls):
        if inspect.isclass(cls):
            self.routes[self.url] = cls()
        else:
            self.routes[self.url] = cls

        def wrapper(*args, **kwargs):
            return self.routes[self.url](*args, **kwargs)
        return wrapper


class Debug:
    def __init__(self):
        pass

    def __call__(self, cls):
        if inspect.isclass(cls):
            method = cls()
        else:
            method = cls

        def wrapper(*args, **kwargs):
            ts = time()
            result = method(*args, **kwargs)
            te = time()
            delta = te - ts
            print(f'debug --> {cls.__name__} выполнялся {delta:2.3f} ms')

            return result
        return wrapper


class Debug2:
    def __init__(self, name=None):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            """
            нужен для того, чтобы декоратор класса wrapper обернул в timeit
            каждый метод декорируемого класса
            """

            def timed(*args, **kw):
                name = self.name if self.name else cls.__name__
                ts = time()
                result = method(*args, **kw)
                te = time()
                delta = te - ts

                print(f'debug --> {name} выполнялся {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)
