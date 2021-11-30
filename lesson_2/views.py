from framework import Jinja2Templates, Request
from patterns.behavioral_patterns import CreateView, ListView, BaseSerializer, EmailNotifier, SmsNotifier
from patterns.structural_patterns import AppRoute, Debug
from patterns.сreational_patterns import Engine, Logger, UserClient

templates = Jinja2Templates(directory='templates/')
site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


@AppRoute('/')
@Debug()
def index_view(_request: Request):
    context = {
        'categories': site.categories
    }
    content = templates.template_response('index.html', context=context)
    return '200 OK', [content.encode('utf-8')]


@AppRoute('/user/registration/')
class UserCreateView(CreateView):
    template_name = 'registration.html'

    def create_obj(self, data: dict):
        user = site.create_user('client', data['email'], data['passwd'])
        site.users.append(user)


@AppRoute('/user/users/')
class UserListView(ListView):
    queryset = site.users
    template_name = 'users_list.html'


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
        logger.log('Категорий товаров')
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
        logger.log('Список категорий товаров')
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
            product.observers.append(email_notifier)
            product.observers.append(sms_notifier)
            product.notify()

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


@AppRoute('/api/products/')
@Debug()
class ProductsApi:
    def __call__(self, request):
        content = BaseSerializer(site.products).save()
        request.content_type = 'application/json'
        return '200 OK', [content.encode('utf-8')]
