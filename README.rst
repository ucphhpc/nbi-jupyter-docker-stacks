==========================
nbi-jupyter-docker-stacks
==========================

A collection of docker jupyter notebook images used at `UCPH <https://www.ku.dk/english/>`_.

Deployed notebooks are published at `DockerHub <https://hub.docker.com/u/ucphhpc>`_.

---------------
Getting Started
---------------

Before any of the images can be built, the Dockerfiles for each Notebook has to be generated first.
The reason for this is that by default each notebook defined by a `Jinja2 <https://jinja2docs.readthedocs.io/en/stable/>`__ template.

To ensure that the nessesary libraries are installed to generate the Notebooks, we recommend that you create a virtual environment
and install the associated requiremnets::

	username@hostname:~/jupyter/nbi-jupyter-docker-stacks$ python3 -m virtualenv venv
	username@hostname:~/jupyter/nbi-jupyter-docker-stacks$ source venv
	(venv) username@hostname:~/jupyter/nbi-jupyter-docker-stacks$ pip install -r requirements.txt

Afterwards, you should now be able to use the `init-notebooks.py` script to generate template and render the Jinja2 template files::

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

The Notebooks and the associated GOCD configuration file are generated based on the definitions specified in the `architecture.yml` file.

This entire process can also be simplified by simply executing `make` in the root directory, which will create an initial Python virtual environment and use the current `architecture.yml` file setup to generate the Dockerfiles and the associated GOCD configuration::

	make

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

------------
Contributing
------------

To contribute either a change to an existing Notebook or introduce a new Notebook is fairly "easy".

***************
Making a change
***************

A change can be introduced to one of the current Notebooks, by altering the selected Notebook setup in its associated directory.

For instance, if a change is to be introduced to the datascience-notebook, the change must be applied either to the ``datascience-notebook/Dockerfile.j2`` Jinja template file, its associated Conda environment file ``datascience-notebook/environment.yml``, or the Python ``datascience-notebook/requirements.txt`` file.

Therefore, to introduce a new Python package to the datascience-notebook, the package should be added to the ``datascience-notebook/requirements.txt`` file. Hereafter, the change can be tested by following the steps outlined in the ``Getting Started``, ``Building``, and ``Testing`` sections above.

In addition, if the change involves introducing a new feature, such as a new Python package, it is prudent that the introduction also ensures that the new package is tested as part of the Notebook image. To accomplish this, a Jupyter Notebook test file should be added, that validates that the added package functions as expected in the Notebooks associated ``tests`` directory. For example, if the `numpy` package was introduced into the datascience-notebook, a test Notebook such as the ``datascience-notebook/tests/numpy.ipynb`` should be included.
