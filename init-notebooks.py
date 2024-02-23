import argparse
import os
import yaml
from jinja2 import Template
from setup.io import load, write, copy

current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(current_dir)

PACKAGE_NAME = "generate-gocd-config"
REPO_NAME = "nbi-jupyter-docker-stacks"
gocd_format_version = 10


def get_pipelines(notebooks):
    pipelines = []
    for notebook, versions in notebooks.items():
        for version, build_data in versions.items():
            notebook_version_name = "{}-{}".format(notebook, version)
            pipelines.append(notebook_version_name)
    return pipelines


def get_common_environment(pipelines, branch="master"):
    common_environment = {
        "environments": {
            "notebook_image_{}".format(branch): {
                "environment_variables": {
                    "DOCKERHUB_USERNAME": "{{SECRET:[dockerhub][username]}}",
                    "DOCKERHUB_PASSWORD": "{{SECRET:[dockerhub][password]}}",
                },
                "pipelines": pipelines,
            }
        }
    }
    return common_environment


def get_common_pipeline():
    common_pipeline = {
        "group": "notebook_image",
        "label_template": "${COUNT}",
        "lock_behaviour": "none",
        # Run on the 1st at 00:00 of every month
        "timer": {
            "spec": "0 0 0 1 * ?",
            "only_on_changes": "no"
        },
        "display_order": -1,
        "template": "notebook_image",
    }
    return common_pipeline


def get_common_materials():
    common_materials = {
        "ucphhpc_images": {
            "git": "https://github.com/ucphhpc/nbi-jupyter-docker-stacks.git",
            "branch": branch,
            "destination": REPO_NAME,
        },
        # this is the name of material
        # says about type of material and url at once
        "publish_docker_git": {
            "git": "https://github.com/rasmunk/publish-docker-scripts.git",
            "branch": "main",
            "username": "${GIT_USER}",
            "password": "{{SECRET:[github][access_token]}}",
            "destination": "publish-docker-scripts",
        },
    }
    return common_materials


def get_upstream_materials(name, pipeline, stage):
    upstream_materials = {
        "upstream_{}".format(name): {
            "pipeline": pipeline,
            "stage": stage,
        }
    }

    return upstream_materials


def get_materials(notebook, upstream_pipeline=None, stage=None):
    materials = {}
    common_materials = get_common_materials()
    materials.update(common_materials)
    if upstream_pipeline and stage:
        upstream_materials = get_upstream_materials(notebook, upstream_pipeline, stage)
        materials.update(upstream_materials)
    return materials


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=PACKAGE_NAME)
    parser.add_argument(
        "--architecture-name",
        default="architecture.yml",
        help="The name of the architecture file that is used to configure the notebooks to be built",
    )
    parser.add_argument(
        "--config-name", default="1.gocd.yml", help="Name of the output gocd config"
    )
    parser.add_argument(
        "--branch", default="master", help="The branch that should be built"
    )
    parser.add_argument(
        "--tag", default="latest", help="The tag that should be built"
    )
    parser.add_argument(
        "--makefile", default="Makefile", help="The makefile that defines the images"
    )
    args = parser.parse_args()

    architecture_name = args.architecture_name
    config_name = args.config_name
    branch = args.branch
    tag = args.tag
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

    list_notebooks = list(notebooks.keys())
    num_notebooks = len(list_notebooks) - 1

    print()
    # Get all pipelines
    pipelines = get_pipelines(notebooks)

    # GOCD environment
    common_environments = get_common_environment(pipelines, branch=branch)

    # Common GOCD pipeline params
    common_pipeline_attributes = get_common_pipeline()

    generated_config = {
        "format_version": gocd_format_version,
        **common_environments,
        "pipelines": {},
    }

    # Generate the notebook Dockerfiles
    for notebook, versions in notebooks.items():
        for version, build_data in versions.items():
            parent = build_data.get("parent", None)
            if not parent:
                print("Missing required parent for notebook: {}".format(notebook))
                exit(-2)

            if "owner" not in parent:
                print("Missing required parent attribute 'owner': {}".format(notebook))
                exit(-2)

            if "image" not in parent:
                print("Missing required parent attribute 'image': {}".format(notebook))
                exit(-2)

            if "tag" not in parent:
                print("Missing required parent attribute 'tag': {}".format(notebook))
                exit(-2)

            parent_image = "{}/{}:{}".format(
                parent["owner"], parent["image"], parent["tag"]
            )

            template_file = build_data.get("file", "{}/Dockerfile.j2".format(notebook))
            output_file = "{}/Dockerfile.{}".format(notebook, version)
            template_content = load(template_file)
            if not template_content:
                print("Could not find the template file: {}".format(template_file))
                exit(-3)

            template = Template(template_content)
            output_content = None
            template_parameters = {"parent": parent_image}

            extra_template_file = build_data.get("extra_template", None)
            if extra_template_file:
                extra_template = load(extra_template_file)
                template_parameters["extra_template"] = extra_template

                # Check for additional template files that should
                # be copied over.
                extra_template_files = build_data.get("extra_template_files", [])
                target_dir = os.path.join(current_dir, notebook)
                for extra_file_path in extra_template_files:
                    extra_file_name = extra_file_path.split("/")[-1]
                    success, msg = copy(
                        extra_file_path, os.path.join(target_dir, extra_file_name)
                    )
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
        for version, build_data in versions.items():
            test_notebook = "{}/{}:{}".format(owner, notebook, version)

            test_template_file = os.path.join("res", "tests", "Dockerfile.test.j2")
            test_output_file = "{}/Dockerfile.{}.test".format(notebook, version)
            test_template_content = load(test_template_file)
            if not test_template_content:
                print(
                    "Could not find test template file: {}".format(test_template_file)
                )
                exit(-4)

            template = Template(test_template_content)
            test_output_content = template.render(parent=test_notebook)
            # Save the rendered template to a file
            write(test_output_file, test_output_content)

    # Generate the GOCD build config
    for notebook, versions in notebooks.items():
        for version, build_data in versions.items():
            parent = build_data.get("parent", None)
            if (
                parent
                and "pipeline_dependent" in parent
                and parent["pipeline_dependent"]
            ):
                parent_pipeline = "{}-{}".format(parent["image"], parent["tag"])
                materials = get_materials(
                    notebook, upstream_pipeline=parent_pipeline, stage="push"
                )
            else:
                materials = get_materials(notebook)

            notebook_version_name = "{}-{}".format(notebook, version)
            notebook_pipeline = {
                **common_pipeline_attributes,
                "materials": materials,
                "parameters": {
                    "NOTEBOOK": notebook,
                    "NOTEBOOK_PIPELINE": notebook_version_name,
                    "DEFAULT_TAG": version,
                    "COMMIT_TAG": "GO_REVISION_UCPHHPC_IMAGES",
                    "EXTRA_TAG": "",
                    "SRC_DIRECTORY": REPO_NAME,
                    "TEST_DIRECTORY": REPO_NAME,
                    "PUSH_DIRECTORY": "publish-docker-scripts",
                    "ARGS": "",
                },
            }
            generated_config["pipelines"][notebook_version_name] = notebook_pipeline

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
                images_declaration += "{} ".format(notebook)
            new_makefile_content.append(images_declaration)
            new_makefile_content.append("\n")
        else:
            new_makefile_content.append(line)

    # Write the new makefile content to the Makefile
    write(makefile_path, new_makefile_content)
    print("Generated a new Makefile in: {}".format(makefile_path))
