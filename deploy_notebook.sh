make build/"${NOTEBOOK}" TAG="${COMMIT}"
make build/"${NOTEBOOK}" TAG="${RELEASE_VERS}"
make push/"${NOTEBOOK}" TAG="${COMMIT}"
make push/"${NOTEBOOK}" TAG="${RELEASE_VERS}"