import os
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from ganzo.cli import run

_tests_root = Path(__file__).parent


def _cleanup(directory: str):
    shutil.rmtree(os.path.abspath(directory))


@patch("builtins.print")
def test_local_list_cli(mock_print: Mock):
    # Given
    templates_path = str(_tests_root.joinpath("fixtures", "templates"))
    args = ["--local-source", templates_path, "--legacy", "list"]

    # When
    run(args)

    # Then
    actuals = list(map(lambda c: c[0][0], mock_print.call_args_list))
    expecteds = ["example"]
    assert len(actuals) == len(expecteds)
    assert all(actual == expected for actual, expected in zip(actuals, expecteds))


def test_local_load_cli():
    # Given
    templates_path = str(_tests_root.joinpath("fixtures", "templates"))
    project_path = str(_tests_root.joinpath("test_project_1"))
    args = [
        "--local-source",
        templates_path,
        "--legacy",
        "load",
        "example",
        project_path,
        "test_project",
    ]

    # When
    run(args)

    # Then
    assert os.path.exists(project_path)
    assert os.path.exists(os.path.join(project_path, "some_file.txt"))
    assert os.path.exists(os.path.join(project_path, "another_file.txt"))

    _cleanup(project_path)


@patch("builtins.print")
def test_local_git_list_cli(mock_print: Mock):
    # Given
    templates_path = str(_tests_root.joinpath("fixtures", "templates"))
    args = ["--local-source", templates_path, "list"]

    # When
    run(args)

    # Then
    actuals = list(map(lambda c: c[0][0], mock_print.call_args_list))
    expecteds = ["example https://github.com/521xueweihan/HelloGitHub.git master"]
    assert len(actuals) == len(expecteds)
    assert all(actual == expected for actual, expected in zip(actuals, expecteds))


def test_local_git_load_cli():
    # Given
    templates_path = str(_tests_root.joinpath("fixtures", "templates"))
    project_path = str(_tests_root.joinpath("test_project_3"))
    args = [
        "--local-source",
        templates_path,
        "load",
        "example",
        project_path,
        "test_project",
    ]

    # When
    run(args)

    # Then
    assert os.path.exists(project_path)
    assert os.path.exists(os.path.join(project_path, "README.md"))
    assert os.path.exists(os.path.join(project_path, ".gitignore"))
    assert not os.path.exists(os.path.join(project_path, ".git"))

    _cleanup(project_path)


@patch("builtins.print")
def test_gcp_list_cli(mock_print: Mock):
    # Given
    args = ["--legacy", "list"]

    # When
    run(args)

    # Then
    actuals = list(map(lambda c: c[0][0], mock_print.call_args_list))
    expecteds = ["app", "lib"]
    assert all(actual == expected for actual, expected in zip(actuals, expecteds))


def test_gcp_load_cli():
    # Given
    project_path = str(_tests_root.joinpath("test_project_2"))
    args = ["--legacy", "load", "app", project_path, "test_project"]

    # When
    run(args)

    # Then
    assert os.path.exists(project_path)
    assert os.path.exists(os.path.join(project_path, "README.md"))

    _cleanup(project_path)
