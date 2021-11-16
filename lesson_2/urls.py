from views import index_view, tools_view, Other, registration_view, login_view

routes = {
    '/': index_view,
    '/category/power-tool/': index_view,
    '/user/registration/': registration_view,
    '/user/login/': login_view,

    '/category/hand-tool/': tools_view,
    '/category/measuring-tool/': tools_view,
    '/category/machine-tools/': tools_view,
    '/category/expendable-materials/': tools_view,

    '/other/': Other()
}
