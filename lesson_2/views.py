from framework import Jinja2Templates, Request

templates = Jinja2Templates(directory='templates/')


def index_view(request: Request):
    print(request)
    products = [
        {
            'title': 'Metabo KGS 216 M',
            'text': 'Торцовая пила Metabo KGS 216 M',
            'image': 'c9155a41899f7e0062e8d7676eccc567.jpg',
            'price': 23299,
        },
        {
            'title': 'Stanley STGS9125',
            'text': 'Угловая шлифовальная машина Stanley STGS9125',
            'image': '126a408b19af26aa9c95716da5bf0bc7.jpg',
            'price': 3059,
        },
        {
            'title': 'DeWalt DCD771D2',
            'text': 'Аккумуляторная дрель-шуруповерт DeWalt DCD771D2',
            'image': '6a90b241830c10350ed0c247ac253796.png',
            'price': 11289,
        },
        {
            'title': 'Bosch GST 150 ВСЕ',
            'text': 'Лобзик Bosch GST 150 ВСЕ',
            'image': 'ebda01400c7d7b510acf55422bd91ac9.jpg',
            'price': 17199,
        },
        {
            'title': 'Bosch GDX + GBH 180-LI',
            'text': 'Аккумуляторный набор Bosch GDX 180-LI + GBH 180-LI',
            'image': 'b62279870d46915744223ef5a7779841.jpg',
            'price': 32989,
        },
    ]

    context = {
        'products': products,
    }
    content = templates.template_response('index.html', context=context)
    return '200 OK', [content.encode('utf-8')]


def registration_view(request: Request):
    if request.method == 'POST':
        print('Регистрация: ', request.data)
    content = templates.template_response('registration.html')
    return '200 OK', [content.encode('utf-8')]


def login_view(request: Request):
    print(request.params)
    return index_view(request)


def tools_view(request: Request):
    print(request)
    content = templates.template_response('tools.html')
    return '200 OK', [content.encode('utf-8')]


class Other:
    def __call__(self, request: Request):
        print(request)
        content = templates.template_response('tools.html')
        return '200 OK', [content.encode('utf-8')]
