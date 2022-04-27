.PHONY: help all clean build build-all maintainer-clean install-dep uninstall-dep
.PHONY: installcheck uninstallcheck test test-all push push-all

OWNER:=nielsbohr
TAG:=edge
PACKAGE_TIMEOUT:=60
ALL_IMAGES:=base-notebook python-notebook r-notebook slurm-notebook python-cuda-notebook gpu-notebook dgx1-notebook datascience-notebook chemistry-notebook fenics-notebook qsharp-notebook hpc-gpu-notebook hpc-notebook hpc-ocean-notebook ocean-notebook geo-notebook bio-notebook bio-bigdata-notebook bio-bsa-notebook sme-notebook jwst-notebook 

all: venv install-dep help

# Inspired by https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@echo "nbi-jupyter-docker-stacks"
	@echo "========================="
	@echo "Replace % with a notebook directory name (e.g., make build/base-notebook)"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean:
	rm -fr .env
	rm -fr .pytest_cache
	rm -fr tests/__pycache__

build/%:
	docker build --rm --force-rm -t $(OWNER)/$(notdir $@):$(TAG) -f ./$(notdir $@)/Dockerfile.${TAG} --build-arg PACKAGE_TIMEOUT=${PACKAGE_TIMEOUT} ${ARGS} ./$(notdir $@)

build-all: $(foreach i,$(ALL_IMAGES),build/$(i))

maintainer-clean:
	@echo 'This command is intended for maintainers to use; it'
	@echo 'deletes files that may need special tools to rebuild.'
	$(MAKE) venv-clean

install-dev:
	$(VENV)/pip install -r requirements-dev.txt

install-dep:
	$(VENV)/pip install -r requirements.txt

uninstall-dep:
	$(VENV)/pip uninstall -r requirements.txt

installcheck:
	$(VENV)/pip install -r tests/requirements.txt

uninstallcheck:
	$(VENV)/pip uninstall -y -r requirements.txt

test/%:
	$(MAKE) build/$(notdir $@)
	docker build --rm --force-rm -t $(OWNER)/$(notdir $@):$(TAG)-test -f ./$(notdir $@)/Dockerfile.${TAG}.test ${ARGS} ./$(notdir $@)
	docker run $(OWNER)/$(notdir $@):$(TAG)-test

test-all: $(foreach i, $(ALL_IMAGES),test/$(i))

push/%:
	docker push $(OWNER)/$(notdir $@):$(TAG)

push-all: $(foreach i, $(ALL_IMAGES),build/$(i) push/$(i))

include Makefile.venv