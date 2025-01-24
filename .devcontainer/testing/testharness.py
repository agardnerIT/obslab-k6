import subprocess
import os
from helpers import *

steps = get_steps(f"/workspaces/{REPOSITORY_NAME}/.devcontainer/testing/steps.txt")
INSTALL_PLAYWRIGHT_BROWSERS = False

# Installing Browsers for Playwright is a time consuming task
# So only install if we need to
# That means if running in non-dev mode (dev mode assumes the person already has everything installed)
# AND the steps file actually contains a playwright test (no point otherwise!)
if DEV_MODE == "FALSE":
    for step in steps:
        if "test_" in step:
            INSTALL_PLAYWRIGHT_BROWSERS = True

if INSTALL_PLAYWRIGHT_BROWSERS:
    subprocess.run(["playwright", "install", "chromium-headless-shell", "--only-shell"])

for step in steps:
    step = step.strip()

    if step.startswith("//") or step.startswith("#"):
        print(f"[{step}] Ignore this step. It is commented out.")
        continue
    
    if "test_" in step:
        print(f"[{step}] This step is a Playwright test.")
        if DEV_MODE == "FALSE": # Standard mode. Run test headlessly
            output = subprocess.run(["pytest", "--capture=no", f"{TESTING_BASE_DIR}/{step}"], capture_output=True, text=True)
        else: # Interactive mode (when a maintainer is improving testing. Spin up the browser visually.
            output = subprocess.run(["pytest", "--capture=no", "--headed", f"{TESTING_BASE_DIR}/{step}"], capture_output=True, text=True)

        if output.returncode != 0 and DEV_MODE == "FALSE":
            logger.error(f"Must create an issue: {step} {output}")
            create_github_issue(output, step_name=step)
        else:
            print(output)
    else:
        output = subprocess.run(["runme", "run", step], capture_output=True, text=True)
        print(f"[{step}] | {output.returncode} | {output.stdout}")
        if output.returncode != 0 and DEV_MODE == "FALSE":
            logger.error(f"Must create an issue: {step} {output}")
            logger.error("Must create an issue...")
            create_github_issue(output, step_name=step)
        else:
            print(output)
