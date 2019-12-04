#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

APPLICATION_NAME=${APPLICATION_NAME:-odh-landscape}
ROUTE_NAME=${ROUTE_NAME:-odh-landscape}
REPLICAS=${REPLICAS:-1}
IMAGE_REPOSITORY=${IMAGE_REPOSITORY:-quay.io/opendatahub/odh-landscape:latest}

echo "Deploying ${IMAGE_REPOSITORY}"

oc create secret docker-registry ${APPLICATION_NAME}-pull \
  --docker-server=${IMAGE_REGISTRY} \
  --docker-username=${IMAGE_REGISTRY_USERNAME} \
  --docker-password=${IMAGE_REGISTRY_PASSWORD} \
  --docker-email=${IMAGE_REGISTRY_EMAIL}

oc process -f ${DIR}/templates/webserver.yml \
  -p APPLICATION_NAME=${APPLICATION_NAME} \
  -p ROUTE_NAME=${ROUTE_NAME} \
  -p REPLICAS=${REPLICAS} \
  -p IMAGE_REPOSITORY=${IMAGE_REPOSITORY} \
  | oc create -f -
