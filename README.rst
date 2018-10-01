.. image:: https://travis-ci.org/rasmunk/nbi-jupyter-docker-stacks.svg?branch=master
    :target: https://travis-ci.org/rasmunk/nbi-jupyter-docker-stacks

==========================
nbi-jupyter-docker-stacks
==========================

A collection of docker jupyter notebook images used at https://www.ku.dk/english/.

-----------
Overview
-----------

To build a particular notebook pass the directory name that contains the dockerfile to make::

	make build/base-notebook


This will start the build procedure, the output will be a container image that is tagged with the word "edge".

To change this, override the TAG variable when calling a make target, e.g.::

	make build/base-notebook TAG=latest


The Makefile also provides targets for test and push options. For example, first test the edge tagged image,
then build an official latest tagged image and push it to the preset OWNER variable's dockerhub repository::

	make test/base-notebook
	make build/base-notebook TAG=latest
	make push/base-notebook


To evaluate the entire stack, a target to 'build-all'/'test-all' is also available i.e.::

	make build-all
	make test-all

