import json
import logging
import os

from ganzo.resolvers import resolve_templates
from ganzo.sources.gcs import GCSSource
from ganzo.sources.git import GitSourceWrapper
from ganzo.sources.local import LocalSource

logger = logging.getLogger(__name__)

GANZO_CONFIG_DIR = os.path.join("~", ".ganzo")
GANZO_CONFIG_FILE = "configuration.json"


def load_template_gcs_bucket_name():
    ganzo_home = os.path.expanduser(GANZO_CONFIG_DIR)
    config_file_path = os.path.join(ganzo_home, GANZO_CONFIG_FILE)

    if not os.path.isdir(ganzo_home):
        raise ValueError(f"No configuration folder available at '{ganzo_home}'.")

    if not os.path.isfile(config_file_path):
        raise ValueError(f"No configuration file available at '{config_file_path}'.")

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

    if options.git_power:
        source = GitSourceWrapper(source)

    templates = source.list_templates()
    for template in templates:
        print(template)


def load_template(options):
    if options.local_source:
        source = LocalSource(options.local_source)
    else:
        gcs_bucket_name = load_template_gcs_bucket_name()
        source = GCSSource(gcs_bucket_name)

    if options.git_power:
        source = GitSourceWrapper(source)

    source.load_template(options.template, options.directory)
    resolve_templates(options.directory, {"__PROJECT_NAME__": options.project_name})
