import os
from utils import *
import dotenv

CODESPACE_NAME = os.environ.get("CODESPACE_NAME", "")
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "")

# Install RunMe
RUNME_CLI_VERSION = "3.10.2"
run_command(["mkdir", "runme"])
run_command(["wget", "-O", "runme/runme_linux_x86_64.tar.gz", f"https://download.stateful.com/runme/{RUNME_CLI_VERSION}/runme_linux_x86_64.tar.gz"])
run_command(["tar", "-xvf", "runme/runme_linux_x86_64.tar.gz"])
run_command(["sudo", "mv", "runme/runme /usr/local/bin"])
run_command(["rm", "-rf", "runme"])

# Build DT environment URLs
DT_TENANT_APPS, DT_TENANT_LIVE = build_dt_urls(dt_env_id=DT_ENVIRONMENT_ID, dt_env_type=DT_ENVIRONMENT_TYPE)

# Write .env file
# Required because user interaction needs DT_TENANT_LIVE during the tutorial
# So we tell user to source .env
dotenv.set_key(dotenv_path=".env", key_to_set="DT_URL", value_to_set=DT_TENANT_LIVE, export=True)

if CODESPACE_NAME.startswith("dttest-"):
    # Set default repository for gh CLI
    # Required for the e2e test harness
    # If it needs to interact with GitHub (eg. create an issue for a failed e2e test)
    run_command(["gh", "repo", "set-default", GITHUB_REPOSITORY])

    # Now set up a label, used if / when the e2e test fails
    # This may already be set (when demos are re-executed in repos)
    # so catch error and always return true
    # Otherwise the entire post-start.sh script could fail
    # We can do this as we know we have permission to this repo
    # (because we're the owner and testing it)
    run_command(["gh", "label", "create", "e2e test failed", "--force"])
    run_command(["pip", "install", "-r", "requirements.txt"])
    run_command(["python", "testharness.py"])

    # Testing finished
    # Destroy the codespace
    run_command(["gh", "codespace", "delete", "--codespace", CODESPACE_NAME, "--force"])
#else:
#    send_startup_ping(demo_name="obslab-k6")