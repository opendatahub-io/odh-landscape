#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT_DIR="$(dirname "$DIR")"
SRC_CSV="${ROOT_DIR}/landscape.csv"
DEST_YML="${ROOT_DIR}/landscape.yml"


echo "Importing ${SRC_CSV} and writing ${DEST_YML}"

python3 "${DIR}/import_landscape.py"  "${SRC_CSV}" "${DEST_YML}" && sed -i 's/ null//' "${DEST_YML}" && sed -i "s/''/null/" "${DEST_YML}"

echo "Import complete"
