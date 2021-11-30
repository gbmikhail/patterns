import copy

from patterns.behavioral_patterns import Subject, ConsoleWriter


class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __str__(self):
        return self.name


class UserAdministrator(User):
    pass


class UserClient(User):
    def __init__(self, name, password):
        self.products = []
        super().__init__(name, password)


class UserFactory:
    types = {
        'client': UserClient,
        'administrator': UserAdministrator
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, password):
        assert type_ in cls.types.keys(), f'{type_} not in {cls.types.keys()}'
        return cls.types[type_](name, password)


class Category:
    auto_id = 0

    def __init__(self, name):
        Category.auto_id += 1
        self.id = Category.auto_id
        self.name = name


class ProductPrototype:
    def clone(self):
        Product.auto_id += 1
        product = copy.deepcopy(self)
        product.id = Product.auto_id
        return product


class Product(ProductPrototype, Subject):
    auto_id = 0

    def __init__(self, category: Category, name: str, text: str, image: str, price: float):
        Product.auto_id += 1
        self.id = Product.auto_id
        self.category = category
        self.name = name
        self.text = text
        self.image = image
        self.price = price
        self.users = []
        super().__init__()

    def __getitem__(self, item):
        return self.users[item]

    def add_user(self, user: UserClient):
        self.users.append(user)
        user.products.append(self)
        self.notify()


class Engine:
    def __init__(self):
        self.users = []
        self.categories = [
            Category('Электроинструмент'),
            Category('Ручной инструмент'),
            Category('Измерительный инструмент'),
            Category('Станки'),
            Category('Расходные материалы'),
        ]

        category = self.categories[0]
        self.products = [
            Product(category, 'Metabo KGS 216 M', 'Торцовая пила Metabo KGS 216 M', 'c9155a41899f7e0062e8d7676eccc567.jpg', 23299),
            Product(category, 'Stanley STGS9125', 'Угловая шлифовальная машина Stanley STGS9125', '126a408b19af26aa9c95716da5bf0bc7.jpg', 3059),
            Product(category, 'DeWalt DCD771D2', 'Аккумуляторная дрель-шуруповерт DeWalt DCD771D2', '6a90b241830c10350ed0c247ac253796.png', 11289),
            Product(category, 'Bosch GST 150 ВСЕ', 'Лобзик Bosch GST 150 ВСЕ', 'ebda01400c7d7b510acf55422bd91ac9.jpg', 17199),
            Product(category, 'Bosch GDX + GBH 180-LI', 'Аккумуляторный набор Bosch GDX 180-LI + GBH 180-LI', 'b62279870d46915744223ef5a7779841.jpg', 32989),
        ]

    @staticmethod
    def create_user(type_, name, password):
        return UserFactory.create(type_, name, password)


    @staticmethod
    def create_category(name: str) -> Category:
        return Category(name)

    @staticmethod
    def create_product(category, name, text, image, price) -> Product:
        return Product(category, name, text, image, price)

    def find_category_by_id(self, category_id: int) -> Category:
        for i in self.categories:
            if i.id == category_id:
                return i
        raise Exception(f'Нет категории с id = {category_id}')

    def get_products_by_category_id(self, category_id: int):
        return [x for x in self.products if x.category.id == category_id]

    def get_product_by_name(self, name: str) -> Product:
        for i in self.products:
            if i.name == name:
                return i
        raise Exception(f'Нет товара с именем {name}')

    def get_product_by_id(self, product_id: int) -> Product:
        for i in self.products:
            if i.id == product_id:
                return i
        raise Exception(f'Нет товара с именем {product_id}')


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        name = None
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)
