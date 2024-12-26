#!/bin/bash

# Install runme
RUNME_CLI_VERSION=3.10.2
mkdir runme
cd runme
wget -O runme_linux_x86_64.tar.gz https://download.stateful.com/runme/$RUNME_CLI_VERSION/runme_linux_x86_64.tar.gz
tar -xvf runme_linux_x86_64.tar.gz
sudo mv runme /usr/local/bin
cd ..
rm -rf runme

# Creation Ping
# curl -X POST https://grzxx1q7wd.execute-api.us-east-1.amazonaws.com/default/codespace-tracker \
#   -H "Content-Type: application/json" \
#   -d "{
#     \"tenant\": \"$DT_URL\",
#     \"repo\": \"$GITHUB_REPOSITORY\",
#     \"demo\": \"obslab-k6\",
#     \"codespace.name\": \"$CODESPACE_NAME\"
#   }"
