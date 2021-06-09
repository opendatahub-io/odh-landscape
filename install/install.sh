#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "fetching landscape project..."

cd ${DIR}/../..

# Clone landscape app local
if [ -d "./landscapeapp" ] 
then
    echo "landscapeapp exists" 
else
    echo "cloning landscapeapp..."
    git clone -b ${BRANCH_LOCAL_DEV} ${LANDSCAPE_LOCAL_DEV}
fi


# Setup yarn and install depenencies
cd ./landscapeapp

if ! command -v $(yarn version check) &> /dev/null
then
    echo "Installing yarn"
    npm install --global yarn
fi

yarn

# # install packages globally
# cd ..
# npm install