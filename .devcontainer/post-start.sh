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


# Set secret key to /tmp/secret
python /workspaces/$RepositoryName/set_secret_key.py

nohup fastapi run /workspaces/$RepositoryName/listenserver.py > /dev/null &

# open listenserver port 8000 publicly
gh codespace ports visibility 8000:public -c $CODESPACE_NAME

# Set default repository for gh CLI
# Required for the e2e test harness
# If it needs to interact with GitHub (eg. create an issue for a failed e2e test)
gh repo set-default $GITHUB_REPOSITORY
# Now set up a label, used if / when the e2e test fails
gh label create "e2e test failed"

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
