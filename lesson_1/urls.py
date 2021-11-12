from views import index_view, tools_view, Other

routes = {
    '/': index_view,
    '/category/power-tool/': index_view,
    '/category/hand-tool/': tools_view,
    '/category/measuring-tool/': tools_view,
    '/category/machine-tools/': tools_view,
    '/category/expendable-materials/': tools_view,

    '/other/': Other()
}
