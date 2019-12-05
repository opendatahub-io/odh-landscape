#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

APPLICATION_NAME=${APPLICATION_NAME:-odh-landscape}
ROUTE_NAME=${ROUTE_NAME:-odh-landscape}

oc process -f ${DIR}/templates/webserver.yml \
  -p APPLICATION_NAME=${APPLICATION_NAME} \
  -p ROUTE_NAME=${ROUTE_NAME} \
  | oc delete -f -

oc delete secret ${APPLICATION_NAME}-pull