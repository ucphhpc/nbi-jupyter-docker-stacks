#!/bin/bash
NOTEBOOK=$1
TAG=$2

# Ensure that the TAG parameter is not more than 12 chars
TAG=${TAG}

if [[ -n ${DOCKERHUB_USERNAME} ]] && [[ -n ${DOCKERHUB_PASSWORD} ]]; then
    echo "${DOCKERHUB_PASSWORD}" | docker login -u ${DOCKERHUB_USERNAME} --password-stdin
fi

make build/${NOTEBOOK} TAG=${TAG}
make push/${NOTEBOOK} TAG=${TAG}