import argparse
import sys

from ganzo.core import list_templates, load_template


def run(args=None):
    parser = argparse.ArgumentParser(prog="ganzo")
    sub_parsers = parser.add_subparsers(help="Available commands")
    parser.add_argument(
        "-l",
        "--local-source",
        metavar="LOCAL_TEMPLATES_PATH",
        help="Load templates from local directory.",
    )

    parser.add_argument(
        "-g",
        "--git-power",
        action="store_true",
        help="Load templates from git repositories provided in template list.",
    )

    list_parser = sub_parsers.add_parser("list", help="List available templates")
    list_parser.set_defaults(func=list_templates)

    create_parser = sub_parsers.add_parser(
        "load", help="Load template into target directory"
    )
    create_parser.set_defaults(func=load_template)
    create_parser.add_argument(
        "template",
        metavar="TEMPLATE_NAME",
        help="The name of the template to load.",
    )
    create_parser.add_argument(
        "directory", metavar="DIR_PATH", help="A directory to load the template into."
    )
    create_parser.add_argument(
        "project_name", metavar="PROJECT_NAME", help="Name of the project."
    )

    try:
        options = parser.parse_args(args)
        options.func(options)
    except (AttributeError, ValueError) as exception:
        print("Error:", exception, file=sys.stderr)
        parser.print_help()


def main():
    return_code = 1
    try:
        run()
        return_code = 0
    except Exception as exception:  # pylint: disable=W0703
        print(f"Error: {exception}", file=sys.stderr)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
