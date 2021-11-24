from views import index_view, Other, registration_view, login_view, ToolsView, CreateCategory, CategoryList, \
    ProductsList, CopyProduct, CreateProduct

routes = {
    '/': index_view,
    '/user/registration/': registration_view,
    '/user/login/': login_view,
    '/other/': Other(),

    '/category': ToolsView(),
    '/category/list/': CategoryList(),
    '/category/create/': CreateCategory(),

    '/products/list/': ProductsList(),
    '/products/create/': CreateProduct(),
    '/products/copy': CopyProduct(),
}
