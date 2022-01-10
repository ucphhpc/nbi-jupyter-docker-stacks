import argparse
import os
import yaml
from configure import NOTEBOOKS

current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(current_dir)

PACKAGE_NAME = "generate-gocd-config"
gocd_format_version = 10
branch = "ci_testing"

# GOCD environment
common_environments = {
    "environments": {
        "docker_images": {
            "environment_variables": {
                "RELEASE": "edge",
                "DOCKERHUB_USERNAME": "{{SECRET:[dockerhub][username]}}",
                "DOCKERHUB_PASSWORD": "{{SECRET:[dockerhub][password]}}",
            },
            "pipelines": NOTEBOOKS,
        }
    }
}

# Common GOCD pipeline params
common_pipeline_attributes = {
    "group": "ucphhpc",
    "label_template": "${COUNT}",
    "lock_behaviour": "none",
    "display_order": -1,
    "materials": {
        "nbi_images": {
            "git": "https://github.com/ucphhpc/nbi-jupyter-docker-stacks.git",
            "branch": branch,
        }
    },
    "template": "docker_image",
}


def save_config(path, config, mode="w", handler=yaml, **handler_kwargs):
    try:
        with open(path, mode) as fh:
            if handler:
                handler.dump(config, fh, **handler_kwargs)
            else:
                fh.write(config)
        return True
    except Exception as err:
        print("Failed to save file: {} - {}".format(path, err))
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=PACKAGE_NAME)
    parser.add_argument(
        "--config-name", default="1.gocd.yml", help="Name of the output gocd config"
    )

    args = parser.parse_args()
    config_name = args.config_name

    generated_config = {
        "format_version": gocd_format_version,
        **common_environments,
        "pipelines": {},
    }

    for notebook in NOTEBOOKS:
        notebook_pipeline = {
            **common_pipeline_attributes,
            "parameters": {"NOTEBOOK": notebook},
        }
        generated_config["pipelines"][notebook] = notebook_pipeline

    path = os.path.join(parent_dir, config_name)
    if not save_config(path, generated_config):
        print("Failed to save config")
        exit(-1)
    print("Generated config in: {}".format(path))
