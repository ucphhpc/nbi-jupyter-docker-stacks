#!/bin/bash
NOTEBOOK=$1
TAG=$2

if [[ -n ${DOCKERHUB_USERNAME} ]] && [[ -n ${DOCKERHUB_PASSWORD} ]]; then
    echo "${DOCKERHUB_PASSWORD}" | docker login -u ${DOCKERHUB_USERNAME} --password-stdin
fi

make build/${NOTEBOOK} TAG=${TAG}
make push/${NOTEBOOK} TAG=${TAG}