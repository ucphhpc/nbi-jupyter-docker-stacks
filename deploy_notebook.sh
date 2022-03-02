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
echo "Pre test EXTRA_TAG: ${EXTRA_TAG}"
extra_tag_var_name=${EXTRA_TAG}

if [[ -n ${EXTRA_TAG} ]]; then
    echo "Extra tag: ${extra_tag_var_name}"
    echo "extra tag expanded: ${!extra_tag_var_name}"

    ln -s ${NOTEBOOK}/Dockerfile.${TAG} ${NOTEBOOK}/Dockerfile.${EXTRA_TAG}

    make build/${NOTEBOOK} TAG=${EXTRA_TAG} ARGS=${BUILD_ARGS}
    make push/${NOTEBOOK} TAG=${EXTRA_TAG} ARGS=${BUILD_ARGS}
fi