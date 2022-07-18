import argparse
import json
import logging
import os
import sys

from ganzo.sources import GCSSource

logger = logging.getLogger(__name__)


def load_template_gcs_bucket_name():
    user_home = os.path.expanduser("~")
    config_dir_path = os.path.join(user_home, ".ganzo")
    config_file_path = os.path.join(config_dir_path, "configuration.json")

    if not os.path.isdir(config_dir_path):
        raise ValueError(f"No configuration available at '{config_dir_path}'.")

    with open(config_file_path, "r", encoding="utf8") as config_file:
        config = json.load(config_file)

        if "gcs_bucket_name" in config:
            return config["gcs_bucket_name"]

        raise ValueError(
            f"Configuration attribute 'gcs_bucket_name' not defined in '{config_file_path}'."
        )


def list_templates(_):
    gcs_bucket_name = load_template_gcs_bucket_name()
    source = GCSSource(gcs_bucket_name)
    templates = source.list_templates()
    for template in templates:
        print(template)


def load_template(options):
    gcs_bucket_name = load_template_gcs_bucket_name()
    source = GCSSource(gcs_bucket_name)
    source.load_template(options.template, options.directory)


def run(args=None):
    parser = argparse.ArgumentParser(prog="ganzo")
    sub_parsers = parser.add_subparsers(help="sub-command help")

    list_parser = sub_parsers.add_parser("list", help="list help")
    list_parser.set_defaults(func=list_templates)

    create_parser = sub_parsers.add_parser("load", help="create help")
    create_parser.set_defaults(func=load_template)
    create_parser.add_argument(
        "template", metavar="TEMPLATE_NAME", help="The template to load."
    )
    create_parser.add_argument(
        "directory", metavar="DIR_PATH", help="A directory load the template into."
    )

    try:
        options = parser.parse_args(args)
        options.func(options)
    except (AttributeError, ValueError) as exception:
        print(exception, file=sys.stderr)
        parser.print_help()


def main():
    return_code = 1
    try:
        run()
        return_code = 0
    except Exception as exception:
        print(f"Error: {exception}", file=sys.stderr)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
