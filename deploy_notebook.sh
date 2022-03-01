#!/bin/bash
NOTEBOOK=$1
BUILD_ARGS=$2
TAG=$3
EXTRA_TAG=$4

if [[ -n ${DOCKERHUB_USERNAME} ]] && [[ -n ${DOCKERHUB_PASSWORD} ]]; then
    echo "${DOCKERHUB_PASSWORD}" | docker login -u ${DOCKERHUB_USERNAME} --password-stdin
fi

make build/${NOTEBOOK} TAG=${TAG} ARGS=${BUILD_ARGS}
make push/${NOTEBOOK} TAG=${TAG} ARGS=${BUILD_ARGS}

# If the EXTRA_TAG is set.
# Link it to the original tag and push that version as well
echo "Extra tag ${EXTRA_TAG}"
if [[ -z $EXTRA_TAG ]]; then
    ln -s ${NOTEBOOK}/Dockerfile.${TAG} ${NOTEBOOK}/Dockerfile.${EXTRA_TAG}

    make build/${NOTEBOOK} TAG=${EXTRA_TAG} ARGS=${BUILD_ARGS}
    make push/${NOTEBOOK} TAG=${EXTRA_TAG} ARGS=${BUILD_ARGS}
fi