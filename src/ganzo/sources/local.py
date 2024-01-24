import os
from distutils.dir_util import copy_tree
from typing import List

from ganzo.sources import TemplateSource


class LocalSource(TemplateSource):
    def __init__(
        self,
        base_path: str,
        template_list_file_name: str = "templates.list",
    ):
        self.base_path = base_path
        self.template_list_file_name = template_list_file_name

    def list_templates(self) -> List[str]:
        templates_path = os.path.join(self.base_path, self.template_list_file_name)
        with open(templates_path, "r", encoding="utf-8") as file:
            return file.read().strip().split("\n")

    def load_template(self, template_name: str, target_path: str):
        template_path = os.path.join(self.base_path, template_name)

        print(f"Copying '{template_path}' into '{target_path}'")
        copy_tree(template_path, target_path)
