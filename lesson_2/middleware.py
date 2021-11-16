# Front controllers
from framework import Request


def secret_front(request: Request):
    request.headers['secret'] = 'some secret'


def other_front(request: Request):
    request.headers['key'] = 'key'


fronts = [secret_front, other_front]
