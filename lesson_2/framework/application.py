from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

from .request import Request
from .templating import ViewStatic
from .views import PageNotFound404


class Application:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts
        # Статика будет пока так
        self.static_folder = '/static'

    @staticmethod
    def get_content_type(path: str) -> str:
        if path[-4:] == '.css':
            return 'text/css'
        elif path[-3:] == '.js':
            return 'text/javascript'
        elif path[-4:] == '.jpg' or path[-5:] == '.jpeg':
            return 'image/jpeg'
        elif path[-4:] == '.png':
            return 'image/png'
        else:
            return 'text/html'

    def __call__(self, environ, start_response):
        setup_testing_defaults(environ)

        # TODO: Статика. Временное решение
        path = environ['PATH_INFO']
        if path[: len('/static/')] == '/static/':
            view = ViewStatic(path)
            code, body = view(path)
            start_response(code, [('Content-Type', self.get_content_type(path))])
            return body

        request = Request(environ)
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()
        # front controller
        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', request.content_type)])
        return body

    def run(self, host: str = '127.0.0.1', port: int = 80):
        with make_server(host, port, self) as httpd:
            print(f'Serving on http://{host}:{port}')
            httpd.serve_forever()
