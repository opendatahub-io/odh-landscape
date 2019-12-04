#!/usr/bin/env bash

IMAGE_BUILD_COMMAND=${IMAGE_BUILD_COMMAND:-docker}
IMAGE_REPOSITORY=${IMAGE_REPOSITORY:-quay.io/opendatahub/odh-landscape:latest}

echo "Pushing ${IMAGE_REPOSITORY}"
${IMAGE_BUILD_COMMAND} push ${IMAGE_REPOSITORY}



