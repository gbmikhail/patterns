import copy


class Category:
    auto_id = 0

    def __init__(self, name):
        Category.auto_id += 1
        self.id = Category.auto_id
        self.name = name


class ProductPrototype:
    def clone(self):
        return copy.deepcopy(self)


class Product(ProductPrototype):
    def __init__(self, category: Category, name: str, text: str, image: str, price: float):
        self.category = category
        self.name = name
        self.text = text
        self.image = image
        self.price = price


class Engine:
    def __init__(self):
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
