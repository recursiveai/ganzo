import json
import logging
import os

from ganzo.resolvers import resolve_templates
from ganzo.sources.gcs import GCSSource
from ganzo.sources.local import LocalSource

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


def list_templates(options):
    if options.local_source:
        source = LocalSource(options.local_source)
    else:
        gcs_bucket_name = load_template_gcs_bucket_name()
        source = GCSSource(gcs_bucket_name)

    templates = source.list_templates()
    for template in templates:
        print(template)


def load_template(options):
    if options.local_source:
        source = LocalSource(options.local_source)
    else:
        gcs_bucket_name = load_template_gcs_bucket_name()
        source = GCSSource(gcs_bucket_name)

    source.load_template(options.template, options.directory)
    resolve_templates(options.directory, {"__PROJECT_NAME__": options.project_name})
