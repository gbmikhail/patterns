class PageNotFound404:
    def __call__(self, *args, **kwargs):
        return '404 WHAT', [b'404 Page Not Found']
