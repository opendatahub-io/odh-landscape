#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT_DIR="$(dirname "$DIR")"


echo "Importing landscape.csv and writing landscape.yml"

cd ${DIR}/..
npm install && npm run import-csv
rc=$?
if [[ $rc != 0 ]]; then
  exit $rc;
fi

echo "Import complete"
