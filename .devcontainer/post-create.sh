#!/bin/bash

# Creation Ping
# curl -X POST https://grzxx1q7wd.execute-api.us-east-1.amazonaws.com/default/codespace-tracker \
#   -H "Content-Type: application/json" \
#   -d "{
#     \"tenant\": \"$DT_URL\",
#     \"repo\": \"repo123\",
#     \"demo\": \"obslab-testing\",
#     \"codespace.name\": \"codespace123\"
#   }"