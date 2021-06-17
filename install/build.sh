#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

IMAGE_REPOSITORY=${IMAGE_REPOSITORY:-quay.io/opendatahub/odh-landscape:latest}

echo "Building dist from local"

cd ${DIR}/..
rm -rf dist lookup.json data.json

if [ ! -d "./cached_logos" ]; then
  echo "Creating chached_logos..."
  mkdir cached_logos
fi

npm install && npm run build
rc=$?
if [[ $rc != 0 ]]; then
  exit $rc;
fi