DEFAULT_ENV_FILE := .env
ifneq ("$(wildcard $(DEFAULT_ENV_FILE))","")
include ${DEFAULT_ENV_FILE}
export $(shell sed 's/=.*//' ${DEFAULT_ENV_FILE})
endif

ENV_FILE := .env.local
ifneq ("$(wildcard $(ENV_FILE))","")
include ${ENV_FILE}
export $(shell sed 's/=.*//' ${ENV_FILE})
endif


## Install the project and dependencies
.PHONY: install
install:
	./install/install.sh

## Convert the csv data into the proper landscape format
.PHONY: import
import:
	./install/import.sh

## Build the application
.PHONY: build
build:
	./install/build.sh

## Launches a local development
.PHONY: dev
dev:
	./install/dev.sh

## Push the image to a registry
.PHONY: push
dev:
	./install/push.sh


