#!/bin/bash

# Set default repository for gh CLI
# Required for the e2e test harness
# If it needs to interact with GitHub (eg. create an issue for a failed e2e test)
gh repo set-default $GITHUB_REPOSITORY

# Startup Ping
# curl -X POST https://grzxx1q7wd.execute-api.us-east-1.amazonaws.com/default/codespace-tracker \
#   -H "Content-Type: application/json" \
#   -d "{
#     \"type\": \"com.dynatrace.devrel.handson.codespace.started\",
#     \"tenant\": \"$DT_URL\",
#     \"repo\": \"$GITHUB_REPOSITORY\",
#     \"demo\": \"obslab-k6\",
#     \"codespace.name\": \"$CODESPACE_NAME\"
#   }"
