import subprocess
import os

DEV_MODE = os.environ.get("DEV_MODE", "FALSE").upper() # This is a string. NOT a bool.

def create_github_issue(output):
    subprocess.run(["gh", "issue", "create", "--label", "e2e test failed", "--title", f"Failed on step: {step}", "--body", f"The end to end test script failed on step: {step}\n\n## Error\n```\n{output.stderr}\n```\n\n## Output\n```\n{output.stdout}\n```"])
    exit(0)

# Install Playwright for UI testing
# This ignores the install in DEV_MODE as it assumes you'll have playwright installed already
# For a user repeatedly running app.py (by definition, a user developing this codespace) this saves time
# For the avoidance of doubt: MOST users and scenarios will run app.py ONLY once
# and therefore WANT / NEED the install line to run once.
if DEV_MODE == "FALSE":
    subprocess.run(["playwright", "install", "chromium", "chromium-headless-shell"])

# npx --yes playwright install --with-deps
with open("steps.txt", mode="r") as steps_file:
    steps = steps_file.readlines()

    for step in steps:
        step = step.strip()

        if step.startswith("//") or step.startswith("#"):
            print(f"[{step}] Ignore this step. It is commented out.")
            continue
        
        if "test_" in step:
            print(f"[{step}] This step is a Playwright test.")
            if DEV_MODE == "FALSE":
                output = subprocess.run(["pytest", f"./{step}"], capture_output=True, text=True)
            else:
                output = subprocess.run(["pytest", "--capture=no", "--headed", f"./{step}"], capture_output=True, text=True)

            if output.returncode != 0 and DEV_MODE == "FALSE":
                create_github_issue(output)
            else:
                print(output)
        else:
            output = subprocess.run(["runme", "run", step], capture_output=True, text=True)
            print(f"[{step}] | {output.returncode} | {output.stdout}")
            if output.returncode != 0 and DEV_MODE == "FALSE":
                create_github_issue(output)
            else:
                print(output)