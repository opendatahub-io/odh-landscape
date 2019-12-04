#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd ${DIR}/..
PROJECT_PATH="$PWD" npm explore interactive-landscape -- npm run open:src
