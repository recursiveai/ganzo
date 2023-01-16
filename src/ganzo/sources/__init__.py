from abc import abstractmethod
from typing import List


class TemplateSource:
    @abstractmethod
    def list_templates(self) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def load_template(self, template_name: str, target_path: str) -> None:
        raise NotImplementedError()
