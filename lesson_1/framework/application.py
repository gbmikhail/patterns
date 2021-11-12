from typing import List
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

    def __call__(self, environ, start_response):
        setup_testing_defaults(environ)
        request = Request(
            method=environ['REQUEST_METHOD'],
            base=f"{environ['wsgi.url_scheme']}://{environ['HTTP_HOST']}" +
                 (f":{environ['SERVER_PORT']}" if environ['SERVER_PORT'] != '80' else ''),
            url=environ['PATH_INFO'],
            headers={}
        )

        path = request.url
        if path[: len('/static/')] == '/static/':
            view = ViewStatic(path)
            # TODO: Временное решение
            code, body = view(request)
            start_response(code, [('Content-Type', 'text/css')])
            return body
        elif path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()
        # front controller
        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return body

    def run(self, host: str = '127.0.0.1', port: int = 80):
        with make_server(host, port, self) as httpd:
            print(f'Serving on http://{host}:{port}')
            httpd.serve_forever()
