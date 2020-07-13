ENV_FILE := .env

ifneq ("$(wildcard $(ENV_FILE))","")
include ${ENV_FILE}
export $(shell sed 's/=.*//' ${ENV_FILE})
endif

.PHONY: import
import:
	./install/import.sh

.PHONY: build
build:
	./install/build.sh

.PHONY: dev
dev:
	./install/dev.sh