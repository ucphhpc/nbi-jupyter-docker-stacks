import os
import argparse
from notebooks import NOTEBOOKS

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Configuration script for " "Dockerfile build tags"
    )
    parser.add_argument("-t", "--tag", action="store", default="edge")
    parser.add_argument("-i", "--image", action="store", default="python-noteboook")
    args = parser.parse_args()

    # Replace all FROM tags
    for notebook in NOTEBOOKS:
        path_docker = os.path.join(os.getcwd(), notebook, "Dockerfile")

        with open(path_docker, "r") as f_docker:
            from_line = f_docker.readline()
            content = f_docker.readlines()

        if from_line and content:
            image_tag = from_line.split(":")
            new_from = "".join([image_tag[0], ":", args.tag, "\n"])

            with open(path_docker, "w") as f_docker:
                f_docker.write(new_from)
                f_docker.writelines(content)
