#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

REPLICAS=${REPLICAS:-1}
SOURCE_REPOSITORY_URL=${SOURCE_REPOSITORY_URL:-'https://gitlab.com/opendatahub/odh-landscape.git'}
SOURCE_REPOSITORY_REF=${SOURCE_REPOSITORY_REF:-'master'}
SOURCE_REPOSITORY_DIR=${SOURCE_REPOSITORY_DIR:-'/'}

echo "Creating s2i build on cluster from ${SOURCE_REPOSITORY_URL}:${SOURCE_REPOSITORY_REF}:${SOURCE_REPOSITORY_DIR}"

oc process -f ${DIR}/templates/openshift-build.yml \
  -p REPLICAS=${REPLICAS} \
  -p SOURCE_REPOSITORY_URL=${SOURCE_REPOSITORY_URL} \
  -p SOURCE_REPOSITORY_REF=${SOURCE_REPOSITORY_REF} \
  -p SOURCE_REPOSITORY_DIR=${SOURCE_REPOSITORY_DIR} \
  | oc create -f -


