.PHONY: help

OWNER:=nielsbohr
TAG:=latest

ALL_IMAGES:=base-notebook \
    python-notebook \
    r-notebook \
    SME-notebook

# Inspired by https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@echo "nbi-jupyter-docker-stacks"
	@echo "========================="
	@echo "Replace % with a notebook directory name (e.g., make build/base-notebook)"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build/%: DARGS?=
build/%:
	docker build $(DARGS) --rm --force-rm -t $(OWNER)/$(notdir $@):$(TAG) ./$(notdir $@)

build-all: $(foreach i,$(ALL_IMAGES),build/$(i))