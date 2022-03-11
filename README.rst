==========================
nbi-jupyter-docker-stacks
==========================

A collection of docker jupyter notebook images used at `UCPH <https://www.ku.dk/english/>`_.

Deployed notebooks are published at `DockerHub <https://hub.docker.com/u/nielsbohr>`_.

---------------
Getting Started
---------------

Before any of the images can be built, the Dockerfiles for each Notebook has to be generated first.
The reason for this is that by default each notebook defined by a `Jinja2 <https://jinja2docs.readthedocs.io/en/stable/>`__ template.

To ensure that the nessesary libraries are installed to initialize the repo, we recommend that you create a virtual environment
and install the associated requiremnets::

	username@hostname:~/jupyter/nbi-jupyter-docker-stacks$ python3 -m virtualenv venv
	username@hostname:~/jupyter/nbi-jupyter-docker-stacks$ source venv
	(venv) username@hostname:~/jupyter/nbi-jupyter-docker-stacks$ pip3 install -r requirements.txt

Therefore the `init-notebooks.py` script was developed to generate template and render the Jinja2 template files
with the definitions specified in the `architecture.yml` file::

	(venv) username@hostname:~/jupyter/nbi-jupyter-docker-stacks$ python3 init-notebooks.py 
	Generated the file: hpc-ocean-notebook/Dockerfile.latest
	Generated the file: hpc-ocean-notebook/Dockerfile.20.02.7
	Generated the file: hpc-ocean-notebook/Dockerfile.21.08.0
	Generated the file: ocean-notebook/Dockerfile.latest
	Generated the file: geo-notebook/Dockerfile.latest
	Generated the file: bio-notebook/Dockerfile.latest
	Generated the file: bio-bigdata-notebook/Dockerfile.latest
	Generated the file: bio-bsa-notebook/Dockerfile.latest
	Generated the file: sme-notebook/Dockerfile.latest
	Generated the file: jwst-notebook/Dockerfile.latest
	Generated a new GOCD config in: ...jupyter/nbi-jupyter-docker-stacks/1.gocd.yml
	Generated a new Makefile in: .../jupyter/nbi-jupyter-docker-stacks/Makefile

In addition to generating the Dockerfiles, the `init-notebooks.py` script also generates 
a GOCD configuration and an up-to-date Makefile configuration.

The GOCD `1.gocd.yml` configuration file is used to automatically build and test the defined notebook
pipelines as part of the UCPH CI/CD infrastructure.

--------
Building
--------

After the repository has been configured with the `init-notebooks.py` script as specified in the Getting Started section,
every notebook is ready to be built.

To build a particular notebook pass the directory name that contains the Dockerfile to make::

	make build/base-notebook TAG=latest

This will start the build procedure, the output will be a container image that is tagged with the word "latest".

To change this, override the TAG variable when calling a make target, e.g.::

	make build/base-notebook TAG=edge

However, the Makefile expects that a Dockerfile is available that has the specified TAG as a postfix.
For instance, when using TAG=edge for the `base-notebook`, the Makefile requires that there is a base-notebook/Dockerfile.edge file.

-------
Testing
-------

The Makefile also provides targets for test and push options. For example, first test the edge tagged image,
then build an official latest tagged image and push it to the preset OWNER variable's dockerhub repository::

	make test/base-notebook TAG=latest
	make build/base-notebook TAG=latest
	make push/base-notebook TAG=latest


To evaluate the entire stack, a target to 'build-all'/'test-all' is also available i.e.::

	make build-all
	make test-all
