#!/bin/bash
NOTEBOOK=$1
BUILD_ARGS=$2
TAG=$3



if [[ -n ${DOCKERHUB_USERNAME} ]] && [[ -n ${DOCKERHUB_PASSWORD} ]]; then
    echo "${DOCKERHUB_PASSWORD}" | docker login -u ${DOCKERHUB_USERNAME} --password-stdin
fi

make build/${NOTEBOOK} TAG=${TAG} ARGS=${BUILD_ARGS}
make push/${NOTEBOOK} TAG=${TAG} ARGS=${BUILD_ARGS}