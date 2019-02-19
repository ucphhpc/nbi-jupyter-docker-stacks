import os
import argparse

parser = argparse.ArgumentParser(description='Configuration script for Dockerfile '
                                             'build tags')
parser.add_argument('-t', '--tag', action='store', default='edge')
parser.add_argument('-i', '--image', action='store', default='python-noteboook')
args = parser.parse_args()

IMAGES = ['python-notebook',
          'datascience-notebook',
          'chemistry-notebook',
          'dgx1-notebook',
          'r-notebook',
          'slurm-notebook',
          'hpc-notebook',
          'sme-notebook',
          'statistics-notebook',
          'tensorflow-notebook',
          'thin-notebook']

if __name__ == "__main__":
    # Replace all FROM tags
    for i in IMAGES:
        path_docker = os.path.join(os.getcwd(), i, 'Dockerfile')

        with open(path_docker, 'r') as f_docker:
            from_line = f_docker.readline()
            content = f_docker.readlines()

        if from_line is not None and content is not None:
            image_tag = from_line.split(":")
            new_from = ''.join([image_tag[0], ":", args.tag, "\n"])

            with open(path_docker, 'w') as f_docker:
                f_docker.write(new_from)
                f_docker.writelines(content)
