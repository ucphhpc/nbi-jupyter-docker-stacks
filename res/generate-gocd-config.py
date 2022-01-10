import argparse
import os
import yaml
from configure import NOTEBOOKS

current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(current_dir)

PACKAGE_NAME = "generate-gocd-config"
gocd_format_version = 10


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
    parser.add_argument(
        "--branch", default="master", help="The branch that should be built"
    )
    parser.add_argument(
        "--image-tag",
        default="latest",
        help="The tag that should be used to tag the images",
    )
    args = parser.parse_args()

    config_name = args.config_name
    branch = args.branch
    image_tag = args.image_tag

    # GOCD environment
    common_environments = {
        "environments": {
            "docker_images": {
                "environment_variables": {
                    "RELEASE": image_tag,
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
            "ucphhpc_images": {
                "git": "https://github.com/ucphhpc/nbi-jupyter-docker-stacks.git",
                "branch": branch,
            }
        },
        "template": "notebook_image",
    }

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
