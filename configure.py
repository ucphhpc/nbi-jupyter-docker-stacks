import os
import argparse

parser = argparse.ArgumentParser(
    description="Configuration script for " "Dockerfile build tags"
)
parser.add_argument("-t", "--tag", action="store", default="edge")
parser.add_argument("-i", "--image", action="store", default="python-noteboook")
args = parser.parse_args()

IMAGES = [
    "r-notebook",
    "slurm-notebook",
    "python-notebook",
    "python-cuda-notebook",
    "gpu-notebook",
    "dgx1-notebook",
    "datascience-notebook",
    "chemistry-notebook",
    "fenics-notebook",
    "qsharp-notebook",
    "statistics-notebook",
    "tomography-notebook",
    "hpc-notebook",
    "hpc-ocean-notebook",
    "ocean-notebook",
    "geo-notebook",
    "bio-notebook",
    "sme-notebook",
]

if __name__ == "__main__":
    # Replace all FROM tags
    for i in IMAGES:
        path_docker = os.path.join(os.getcwd(), i, "Dockerfile")

        with open(path_docker, "r") as f_docker:
            from_line = f_docker.readline()
            content = f_docker.readlines()

        if from_line and content:
            image_tag = from_line.split(":")
            new_from = "".join([image_tag[0], ":", args.tag, "\n"])

            with open(path_docker, "w") as f_docker:
                f_docker.write(new_from)
                f_docker.writelines(content)
