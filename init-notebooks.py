import argparse
import os
import yaml
from jinja2 import Template
from setup.io import load, write

current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(current_dir)

PACKAGE_NAME = "generate-gocd-config"
gocd_format_version = 10


def get_common_environment(notebooks):
    common_environment = {
        "environments": {
            "docker_images": {
                "environment_variables": {
                    "DOCKERHUB_USERNAME": "{{SECRET:[dockerhub][username]}}",
                    "DOCKERHUB_PASSWORD": "{{SECRET:[dockerhub][password]}}",
                },
                "pipelines": notebooks,
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=PACKAGE_NAME)
    parser.add_argument(
        "--architecture-name", default="architecture.yml", help="The name of the architecture file that is used to configure the notebooks to be built"
    )
    parser.add_argument(
        "--config-name", default="1.gocd.yml", help="Name of the output gocd config"
    )
    parser.add_argument(
        "--branch", default="master", help="The branch that should be built"
    )
    args = parser.parse_args()

    architecture_name = args.architecture_name
    config_name = args.config_name
    branch = args.branch

    # Load the architecture file
    architecture_path = os.path.join(current_dir, architecture_name)
    architecture = load(architecture_path, handler=yaml, Loader=yaml.FullLoader)
    notebooks = architecture.get("architecture", None)
    if not notebooks:
        print("Failed to load architecture in: {}".format(architecture_path))
        exit(-1)

    list_notebooks = list(key.replace("_", "-") for key in notebooks.keys())
    # GOCD environment
    common_environments = get_common_environment(list(notebooks.keys()))

    # Common GOCD pipeline params
    common_pipeline_attributes = get_common_pipeline()

    generated_config = {
        "format_version": gocd_format_version,
        **common_environments,
        "pipelines": {},
    }

    # Generate the notebook Dockerfiles
    for notebook, versions in notebooks.items():
        name = notebook.replace("_", "-")
        for version, build_data in versions.items():
            parent = build_data.get("parent", None)
            if not parent:
                print("Missing required parent for notebook: {}".format(name))
                exit(-2)

            template_file = build_data.get("file", "{}/Dockerfile.j2".format(name))
            output_file = "{}/Dockerfile.{}".format(name, version)
            template_content = load(template_file)
            if not template_content:
                print("Could not find the template file: {}".format(template_file))
                exit(-3)

            template = Template(template_content)
            output_content = None
            build_parameters = build_data.get("parameters", None)
            if build_parameters:
                # Format the jinja2 template
                output_content = template.render(parent=parent, **build_parameters)
            else:
                output_content = template.render(parent=parent)
            # Save rendered template to a file
            write(output_file, output_content)

    # Generate the GOCD build config
    for notebook, versions in notebooks.items():
        name = notebook.replace("_", "-")
        for version, build_data in versions.items():
            notebook_pipeline = {
                **common_pipeline_attributes,
                "parameters": {
                    "NOTEBOOK": name,
                    "DEFAULT_TAG": version,
                    "COMMIT_TAG": "${GO_REVISION_UCPHHPC_IMAGES}",
                    "ARGS": ""
                },
            }
            generated_config["pipelines"][notebook] = notebook_pipeline

    path = os.path.join(current_dir, config_name)
    if not write(path, generated_config, handler=yaml):
        print("Failed to save config")
        exit(-1)
    print("Generated config in: {}".format(path))
