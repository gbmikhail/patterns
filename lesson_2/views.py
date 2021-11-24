from framework import Jinja2Templates, Request
from patterns.structural_patterns import AppRoute, Debug
from patterns.сreational_patterns import Engine

templates = Jinja2Templates(directory='templates/')
site = Engine()


@AppRoute('/')
@Debug()
def index_view(_request: Request):
    context = {
        'categories': site.categories
    }
    content = templates.template_response('index.html', context=context)
    return '200 OK', [content.encode('utf-8')]


@AppRoute('/user/registration/')
@Debug()
def registration_view(request: Request):
    if request.method == 'POST':
        print('Регистрация: ', request.data)
    content = templates.template_response('registration.html')
    return '200 OK', [content.encode('utf-8')]


@AppRoute('/user/login/')
@Debug()
def login_view(request: Request):
    print(request.params)
    return index_view(request)


@AppRoute('/category')
@Debug()
class ToolsView:
    def __init__(self, _category_id=None):
        # self.category_id = category_id
        pass

    def __call__(self, request: Request):
        category_id = int(request.params['category_id'])
        products = site.get_products_by_category_id(category_id)
        context = {
            'products': products,
            'categories': site.categories
        }
        content = templates.template_response('tools.html', context=context)
        return '200 OK', [content.encode('utf-8')]


@AppRoute('/other/')
@Debug()
class Other:
    def __call__(self, request: Request):
        print(request)
        content = templates.template_response('tools.html')
        return '200 OK', [content.encode('utf-8')]


@AppRoute('/category/list/')
@Debug()
class CategoryList:
    def __call__(self, request):
        context = {
            'categories': site.categories,
        }
        content = templates.template_response('category_list.html', context=context)
        return '200 OK', [content.encode('utf-8')]


@AppRoute('/category/create/')
@Debug()
class CreateCategory:
    def __call__(self, request: Request):
        if request.method == 'POST':
            data = request.data

            name = data['title']
            new_category = site.create_category(name)
            site.categories.append(new_category)

            return CategoryList(request)
        else:
            context = {
                'categories': site.categories,
            }
            content = templates.template_response('create_category.html', context=context)
            return '200 OK', [content.encode('utf-8')]


@AppRoute('/products/create/')
@Debug()
class CreateProduct:
    def __call__(self, request: Request):
        if request.method == 'POST':
            data = request.data
            category_id = int(data['category_id'])

            category = site.find_category_by_id(category_id)
            name = data['name']
            text = data['text']
            image = data['image']
            price = float(data['price'])

            product = site.create_product(category, name, text, image, price)
            site.products.append(product)

            return ProductsList(request)
        else:
            context = {
                'categories': site.categories,
            }
            content = templates.template_response('create_product.html', context=context)
            return '200 OK', [content.encode('utf-8')]


@AppRoute('/products/list/')
@Debug()
class ProductsList:
    def __call__(self, request):
        try:
            context = {
                'categories': site.categories,
                'products': site.products,
            }
            content = templates.template_response('products_list.html', context=context)
            return '200 OK', [content.encode('utf-8')]
        except KeyError:
            return '200 OK', 'No products have been added yet'


@AppRoute('/products/copy')
@Debug()
class CopyProduct:
    def __call__(self, request):
        try:
            product_id = int(request.params['product_id'])
            old = site.get_product_by_id(product_id)
            if old:
                new_product = old.clone()
                new_product.name = f'copy_{new_product.name}'
                site.products.append(new_product)
            return ProductsList(request)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
