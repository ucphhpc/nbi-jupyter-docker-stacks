.PHONY: help

OWNER:=nielsbohr
TAG:=edge
PACKAGE_TIMEOUT:=60


ALL_IMAGES:=base-notebook \
    r-notebook \
    slurm-notebook \
    thin-notebook \
    python-notebook \
    datascience-notebook \
    chemistry-notebook \
    fenics-notebook \
    statistics-notebook \
    tomography-notebook \
    hpc-notebook \
    tensorflow-notebook \
    geo-notebook \
    bio-notebook \
    sme-notebook

# Inspired by https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@echo "nbi-jupyter-docker-stacks"
	@echo "========================="
	@echo "Replace % with a notebook directory name (e.g., make build/base-notebook)"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build/%:
	docker build --rm --force-rm -t $(OWNER)/$(notdir $@):$(TAG) --build-arg PACKAGE_TIMEOUT=${PACKAGE_TIMEOUT} ./$(notdir $@)

build-all: $(foreach i,$(ALL_IMAGES),build/$(i))

test/%:
	$(MAKE) build/$(notdir $@)
	docker build --rm --force-rm -t $(OWNER)/$(notdir $@):$(TAG)-test -f ./$(notdir $@)/Dockerfile.test ./$(notdir $@)
	docker run -it $(OWNER)/$(notdir $@):$(TAG)-test

test-all: $(foreach i, $(ALL_IMAGES),test/$(i))

push/%:
	docker push $(OWNER)/$(notdir $@):$(TAG)

push-all: $(foreach i, $(ALL_IMAGES),build/$(i) push/$(i))
