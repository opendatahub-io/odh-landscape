#!/usr/bin/env bash

APPLICATION_NAME=${APPLICATION_NAME:-odh-landscape}

echo "Rolling out new version of landscape"
oc rollout latest dc/${APPLICATION_NAME}
