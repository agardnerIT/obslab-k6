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

# If this is a testing codespace (codespace names starts with dttest-)
# Install testing dependencies
# and run test harness
if [[ $CODESPACE_NAME == dttest-* ]];
then
  # Set default repository for gh CLI
  # Required for the e2e test harness
  # If it needs to interact with GitHub (eg. create an issue for a failed e2e test)
  gh repo set-default $GITHUB_REPOSITORY
  # Now set up a label, used if / when the e2e test fails
  # This may already be set (when demos are re-executed in repos)
  # so catch error and always return true
  # Otherwise the entire post-start.sh script could fail
  # We can do this as we know we have permission to this repo
  # (because we're the owner and testing it)
  gh label create "e2e test failed" --force
  
  cd /workspaces/$RepositoryName/.devcontainer/testing
  pip install -r requirements.txt
  python testharness.py

  # Testing finished
  # Destroy the codespace
  #gh codespace delete --codespace $CODESPACE_NAME --force
fi

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
