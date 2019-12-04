#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# delete UI
echo "Deleting all parts full s2i build on cluster"

oc process -f ${DIR}/templates/openshift-build.yml | oc delete -f -


