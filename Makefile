.PHONY: help

OWNER:=nielsbohr
TAG:=edge

ALL_IMAGES:=base-notebook \
    python-notebook \
    datascience-notebook \
    dgx1-notebook \
    r-notebook

# Inspired by https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@echo "nbi-jupyter-docker-stacks"
	@echo "========================="
	@echo "Replace % with a notebook directory name (e.g., make build/base-notebook)"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build/%:
	docker build --rm --force-rm -t $(OWNER)/$(notdir $@):$(TAG) ./$(notdir $@)

build-all: $(foreach i,$(ALL_IMAGES),build/$(i))

test/%:
	$(MAKE) build/$(notdir $@)
	docker build --rm --force-rm -t $(OWNER)/$(notdir $@):$(TAG)-test -f ./$(notdir $@)/Dockerfile.test ./$(notdir $@)
	docker run -it $(OWNER)/$(notdir $@):$(TAG)-test

test-all: $(foreach i, $(ALL_IMAGES),test/$(i))

push/%:
	docker push $(OWNER)/$(notdir $@):$(TAG)

push-all: $(foreach i, $(ALL_IMAGES),build/$(i) push/$(i))