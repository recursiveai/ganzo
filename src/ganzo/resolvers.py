import os
from string import Template
from typing import Mapping


def resolve_templates(target_path: str, patterns: Mapping[str, str]):
    with os.scandir(target_path) as entries:
        for entry in entries:
            if entry.is_dir():
                resolve_templates(entry.path, patterns)
            if entry.is_file():
                _resolve_and_replace_file(entry.path, patterns)


def _resolve_and_replace_file(file_path: str, patterns: Mapping[str, str]):
    resolved_file_path, file_ext = os.path.splitext(file_path)
    if file_ext == ".nzo":
        print(f"Resolving '{file_path}' into '{resolved_file_path}'")
        with open(file_path, "r", encoding="utf-8") as source_file:
            file_content = source_file.read()
            content_template = Template(file_content)
            resolved_content = content_template.safe_substitute(**patterns)
            with open(resolved_file_path, "w", encoding="utf-8") as resolved_file:
                resolved_file.write(resolved_content)
        os.remove(file_path)
