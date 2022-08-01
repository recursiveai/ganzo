import os
from distutils.dir_util import copy_tree

from ganzo.sources import TemplateSource


class LocalSource(TemplateSource):
    def __init__(self, base_path: str):
        self.base_path = base_path

    def list_templates(self) -> list[str]:
        templates_path = os.path.join(self.base_path, "templates.list")
        with open(templates_path, "r", encoding="utf-8") as file:
            return file.read().strip().split("\n")

    def load_template(self, template_name: str, target_path: str):
        template_path = os.path.join(self.base_path, template_name)
        print(f"Copying '{template_path}' into '{target_path}'")
        copy_tree(template_path, target_path)
