#!/bin/bash
#
# Launched as the last action of Dockerfile.test after it has installed
# required dependencies like pytest and pytest-xdist plugin with
# pip install -r requirements.txt
# from here.

pytest -n 4 --durations=0
