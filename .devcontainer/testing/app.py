import subprocess
import os

DEV_MODE = os.environ.get("DEV_MODE", "FALSE").upper() # This is a string. NOT a bool.
print(f"DEV_MODE: {DEV_MODE}")

def create_github_issue(output):
    subprocess.run(["gh", "issue", "create", "--label", "e2e test failed", "--title", f"Failed on step: {step}", "--body", f"The end to end test script failed on step: {step}\n\n## Error\n```\n{output.stderr}\n```\n\n## Output\n```\n{output.stdout}\n```"])
    exit(0)

# Install Playwright for UI testing
subprocess.run(["playwright", "install", "chromium", "chromium-headless-shell"])

# npx --yes playwright install --with-deps
with open("steps.txt", mode="r") as steps_file:
    steps = steps_file.readlines()

    for step in steps:
        step = step.strip()

        if step.startswith("//") or step.startswith("#"):
            print(f"Ignore this step. It is commented out: {step}")
            continue
        
        if "test_" in step:
            print(f"This step is a Playwright test: {step}")
            output = subprocess.run(["pytest", f"./{step}"], capture_output=True, text=True)
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