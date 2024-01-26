import shutil
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

    def load_template(
        self,
        template_name: str,
        target_path: str,
    ):
        entries = [template.split(" ") for template in self.list_templates()]
        templates = {entry[0]: (entry[1], entry[2]) for entry in entries}

        if template_name not in templates:
            raise ValueError(f"{template_name} not an available template")

        with tempfile.TemporaryDirectory() as tmp_dir:
            print(f"Cloning {templates[template_name][0]} into '{tmp_dir}'")

            Repo.clone_from(
                templates[template_name][0],
                tmp_dir,
                multi_options=[
                    "--single-branch",
                    f"-b {templates[template_name][1]}",
                ],
            )

            shutil.rmtree(f"{tmp_dir}/.git")

            print(f"Copying {template_name} from '{tmp_dir}' into '{target_path}'")
            copy_tree(tmp_dir, target_path)
