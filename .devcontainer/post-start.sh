#!/bin/bash

# Startup Ping
curl -X POST https://grzxx1q7wd.execute-api.us-east-1.amazonaws.com/default/codespace-tracker \
  -H "Content-Type: application/json" \
  -d "{
    \"type\": \"com.dynatrace.devrel.handson.codespace.started\",
    \"tenant\": \"$DT_URL\",
    \"repo\": \"$GITHUB_REPOSITORY\",
    \"demo\": \"obslab-k6\",
    \"codespace.name\": \"$CODESPACE_NAME\"
  }"