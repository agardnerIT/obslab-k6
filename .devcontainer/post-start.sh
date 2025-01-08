#!/bin/bash

# Get distro information
if [ $(uname -m) = x86_64 ]; then
    ARCH="amd64"
elif [ $(uname -m) = aarch64 ]; then
    ARCH="arm64"
fi

echo "Architecture is ${ARCH}"


# Install runme
RUNME_CLI_VERSION=3.10.2
mkdir runme
cd runme
wget -O runme_linux_${ARCH}.tar.gz https://download.stateful.com/runme/$RUNME_CLI_VERSION/runme_linux_${ARCH}.tar.gz
tar -xvf runme_linux_${ARCH}.tar.gz
sudo mv runme /usr/local/bin
cd ..
rm -rf runme

# Need this if we're not running in CodeSpaces
if [ -z "${RepositoryName}" ]; then
  RepositoryName="obslab-k6"
fi

# Set secret key to /tmp/secret
python /workspaces/$RepositoryName/set_secret_key.py

# If this is a testing codespace (codespace names starts with testing_)
# Install testing dependencies
# and run test harness
if [[ $CODESPACE_NAME == testing_* ]];
then
  cd /workspaces/$RepositoryName/.devcontainer/testing
  pip install -r requirements.txt
  python app.py
fi

pip install -r /workspaces/$RepositoryName/requirements.txt

# Ignore if GH CLI is not installed
if ! command -v gh >/dev/null 2>&1; then
    echo "gh CLI not installed"
else
    # open listenserver port 8000 publicly
    gh codespace ports visibility 8000:public -c $CODESPACE_NAME

    # Set default repository for gh CLI
    # Required for the e2e test harness
    # If it needs to interact with GitHub (eg. create an issue for a failed e2e test)
    gh repo set-default $GITHUB_REPOSITORY
    # Now set up a label, used if / when the e2e test fails
    # This may already be set (when demos are re-executed in repos)
    # so catch error and always return true
    # Otherwise the entire post-start.sh script could fail
    gh label create "e2e test failed" --force
fi

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
