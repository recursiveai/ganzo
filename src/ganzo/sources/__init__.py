from abc import abstractmethod


class TemplateSource:
    @abstractmethod
    def list_templates(self) -> list[str]:
        raise NotImplementedError()

    @abstractmethod
    def load_template(self, template_name: str, target_path: str) -> None:
        raise NotImplementedError()
