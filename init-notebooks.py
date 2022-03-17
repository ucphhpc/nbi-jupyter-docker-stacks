import argparse
from asyncore import read
import os
import yaml
from jinja2 import Template
from setup.io import load, write, copy

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
                "destination": "nbi-jupyter-docker-stacks"
            },
            # this is the name of material
            # says about type of material and url at once
            "publish_docker_git": {
                "git": "https://github.com/rasmunk/publish-docker-scripts.git",
                "branch": "main",
                "username": "${GIT_USER}",
                "password": "{{SECRET:[github][access_token]}}",
                "destination": "publish-docker-scripts"
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
    parser.add_argument(
        "--makefile", default="Makefile", help="The makefile that defines the images"
    )
    args = parser.parse_args()

    architecture_name = args.architecture_name
    config_name = args.config_name
    branch = args.branch
    makefile = args.makefile

    # Load the architecture file
    architecture_path = os.path.join(current_dir, architecture_name)
    architecture = load(architecture_path, handler=yaml, Loader=yaml.FullLoader)
    owner = architecture.get("owner", None)
    if not owner:
        print("Failed to find architecture the owner in: {}".format(architecture_path))
        exit(-1)

    notebooks = architecture.get("architecture", None)
    if not notebooks:
        print("Failed to find the architecture in: {}".format(architecture_path))
        exit(-1)

    list_notebooks = list(key.replace("_", "-") for key in notebooks.keys())
    num_notebooks = len(list_notebooks) - 1

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
            template_parameters = {
                "parent": parent
            }

            extra_template_file = build_data.get("extra_template", None)
            if extra_template_file:
                extra_template = load(extra_template_file)
                template_parameters["extra_template"] = extra_template
                
                # Check for additional template files that should
                # be copied over.
                extra_template_files = build_data.get("extra_template_files", [])
                target_dir = os.path.join(current_dir, name)
                for extra_file_path in extra_template_files:
                    extra_file_name = extra_file_path.split("/")[-1]
                    success, msg = copy(extra_file_path, os.path.join(target_dir, extra_file_name))
                    if not success:
                        print(msg)
                        exit(-4)

            build_parameters = build_data.get("parameters", None)
            if build_parameters:
                template_parameters.update(**build_parameters)

            # Format the jinja2 template
            output_content = template.render(**template_parameters)

            # Save rendered template to a file
            write(output_file, output_content)
            print("Generated the file: {}".format(output_file))
    
    # Generate the test Dockerfiles for the notebooks
    for notebook, versions in notebooks.items():
        name = notebook.replace("_", "-")
        for version, build_data in versions.items():
            test_parent = "{}/{}:{}".format(owner, name, version)

            test_template_file = os.path.join("res", "tests", "Dockerfile.test.j2")
            test_output_file = "{}/Dockerfile.{}.test".format(name, version)
            test_template_content = load(test_template_file)
            if not test_template_content:
                print("Could not find test template file: {}".format(test_template_file))
                exit(-4)

            template = Template(test_template_content)
            test_output_content = template.render(parent=test_parent)
            # Save the rendered template to a file
            write(test_output_file, test_output_content)

    # Generate the GOCD build config
    for notebook, versions in notebooks.items():
        name = notebook.replace("_", "-")
        for version, build_data in versions.items():
            notebook_pipeline = {
                **common_pipeline_attributes,
                "parameters": {
                    "NOTEBOOK": name,
                    "DEFAULT_TAG": version,
                    "SRC_DIRECTORY": name,
                    "TEST_DIRECTORY": name,
                    "PUSH_DIRECTORY": "publish-docker-scripts",
                    "COMMIT_TAG": "GO_REVISION_UCPHHPC_IMAGES",
                    "ARGS": ""
                },
            }
            generated_config["pipelines"][name] = notebook_pipeline

    path = os.path.join(current_dir, config_name)
    if not write(path, generated_config, handler=yaml):
        print("Failed to save config")
        exit(-1)
    print("Generated a new GOCD config in: {}".format(path))

    # Update the Makefile such that it contains every notebook
    # image
    makefile_path = os.path.join(current_dir, makefile)
    makefile_content = load(makefile_path, readlines=True)
    new_makefile_content = []

    for line in makefile_content:
        if "ALL_IMAGES:=" in line:
            images_declaration = "ALL_IMAGES:="
            for notebook in notebooks:
                name = notebook.replace("_", "-")
                images_declaration += "{} ".format(name)
            new_makefile_content.append(images_declaration)
            new_makefile_content.append("\n")
        else:
            new_makefile_content.append(line)

    # Write the new makefile content to the Makefile
    write(makefile_path, new_makefile_content)
    print("Generated a new Makefile in: {}".format(makefile_path))
