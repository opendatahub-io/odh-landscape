#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

IMAGE_REPOSITORY=${IMAGE_REPOSITORY:-quay.io/opendatahub/odh-landscape:latest}

echo "Building dist from local"
#echo "CRUNCHBASE_KEY=${CRUNCHBASE_KEY}"
#echo "GITHUB_KEY=${GITHUB_KEY}"
#echo "TWITTER_KEYS=${TWITTER_KEYS}"


cd ${DIR}/..
rm -rf dist lookup.json data.json
npm install && npm run build
rc=$?
if [[ $rc != 0 ]]; then
  exit $rc;
fi

#s2i build ./dist centos/nginx-114-centos7 ${IMAGE_REPOSITORY}
#echo "Finished building ${IMAGE_REPOSITORY}"
