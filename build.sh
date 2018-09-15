#!/bin/bash
IMAGE_NAME=nielsbohr/base-notebook
IMAGE_VERS=edge

docker build -t $IMAGE_NAME:$IMAGE_VERS .
docker build -t $IMAGE_NAME:$IMAGE_VERS-test -f Dockerfile.test .
