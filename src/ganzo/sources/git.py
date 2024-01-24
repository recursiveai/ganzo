import tempfile
from distutils.dir_util import copy_tree
from typing import List

from git.repo.base import Repo

from ganzo.sources import TemplateSource
from ganzo.sources.gcs import GCSSource
from ganzo.sources.local import LocalSource


class GitSourceWrapper(TemplateSource):
    def __init__(self, source: TemplateSource):
        self.source = source
        if isinstance(source, GCSSource) or isinstance(source, LocalSource):
            source.template_list_file_name = "templates-git.list"
        else:
            raise ValueError(f"{source} not supported")

    def list_templates(self) -> List[str]:
        return self.source.list_templates()

    def load_template(self, template_name: str, target_path: str):
        blah = [template.split(" ") for template in self.list_templates()]
        templates = {key: value for key, value in blah}

        if template_name not in templates:
            raise ValueError(f"{template_name} not an available template")

        with tempfile.TemporaryDirectory() as tmp_dir:
            print(f"Cloning {templates[template_name]} into '{tmp_dir}'")
            repo = Repo.clone_from(templates[template_name], tmp_dir)
            target_branch = repo.create_head("main")
            repo.head.reference = target_branch
            repo.head.reset(index=True, working_tree=True)

            print(f"Copying {template_name} from '{tmp_dir}' into '{target_path}'")
            copy_tree(tmp_dir, target_path)
