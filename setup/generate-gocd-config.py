import argparse
import os
import yaml
from notebooks import NOTEBOOKS
from architecture import NOTEBOOKS_ARCHITECTURE

current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(current_dir)

PACKAGE_NAME = "generate-gocd-config"
gocd_format_version = 10


def get_common_environment():
    common_environment = {
        "environments": {
            "docker_images": {
                "environment_variables": {
                    "DOCKERHUB_USERNAME": "{{SECRET:[dockerhub][username]}}",
                    "DOCKERHUB_PASSWORD": "{{SECRET:[dockerhub][password]}}",
                },
                "pipelines": NOTEBOOKS,
            }
        }
    }
    return common_environment


def get_common_pipeline():
    common_pipeline = {
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
    return common_pipeline


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
        "--default-image-tag",
        default="latest",
        help="Beside the commit specific tagged release, another version is released with this default tag",
    )
    args = parser.parse_args()

    config_name = args.config_name
    branch = args.branch
    default_image_tag = args.default_image_tag

    # GOCD environment
    common_environments = get_common_environment()

    # Common GOCD pipeline params
    common_pipeline_attributes = get_common_pipeline()

    
    generated_config = {
        "format_version": gocd_format_version,
        **common_environments,
        "pipelines": {},
    }

    for notebook in NOTEBOOKS:
        notebook_pipeline = {
            **common_pipeline_attributes,
            "parameters": {
                "NOTEBOOK": notebook,
                "DEFAULT_TAG": default_image_tag,
                "COMMIT_TAG": "${GO_REVISION_UCPHHPC_IMAGES}",
                "BUILD_ARGS": ""
            },
        }
        generated_config["pipelines"][notebook] = notebook_pipeline

    path = os.path.join(parent_dir, config_name)
    if not save_config(path, generated_config):
        print("Failed to save config")
        exit(-1)
    print("Generated config in: {}".format(path))
