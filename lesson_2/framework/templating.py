import os

import jinja2


class Jinja2Templates:
    def __init__(self, *, directory: str):
        self.directory = directory

    def template_response(
            self,
            name: str,
            context: dict = None,
    ) -> str:
        template_loader = jinja2.FileSystemLoader(searchpath=self.directory)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(name)
        if context:
            return template.render(**context)
        return template.render()


class ViewStatic:
    # TODO: Временное решение
    def __init__(self, path: str):
        self.path = path

    def __call__(self, *args, **kwargs):
        file_name = os.path.join(*self.path.split('/'))
        with open(file_name, mode='rb') as f:
            return '200 OK', [f.read()]
