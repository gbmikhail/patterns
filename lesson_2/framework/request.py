from urllib.parse import unquote

from pydantic import BaseModel


class Request(BaseModel):
    method: str
    base: str
    url: str
    headers: dict
    params: dict
    data: dict

    def __init__(self, environ: dict):
        data = {
            'method': environ['REQUEST_METHOD'],
            'base': f"{environ['wsgi.url_scheme']}://{environ['HTTP_HOST']}" +
                    (f":{environ['SERVER_PORT']}" if environ['SERVER_PORT'] != '80' else ''),
            'url': environ['PATH_INFO'],
            'headers': dict(),
            'params': self.get_request_params(environ['QUERY_STRING']),
            'data': self.get_wsgi_input_data(environ)
        }
        super().__init__(**data)

    @staticmethod
    def get_request_params(query_string) -> dict:
        params = dict()
        items = query_string.split('&') if query_string else []
        for i in items:
            key, value = i.split('=')
            params[key] = unquote(value)
        return params

    def get_wsgi_input_data(self, environ) -> dict:
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        if data:
            data_str = data.decode(encoding='utf-8')
            return self.get_request_params(data_str)
        return dict()
