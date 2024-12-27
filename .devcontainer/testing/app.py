import subprocess

# Install Playwright for UI testing
subprocess.run(["playwright", "install"])

# npx --yes playwright install --with-deps
with open("steps.txt", mode="r") as steps_file:
    steps = steps_file.readlines()

    for step in steps:
        step = step.strip()
        if step.startswith("//") or step.startswith("#"):
            print(f"Ignore this step. It is commented out: {step}")
            continue
        
        output = []
        if "test_" in step:
            print(f"This step is a Playwright test: {step}")
            output = subprocess.run(["pytest", "playwright"], capture_output=True, text=True)
        else:
            output = subprocess.run(["runme", "run", step], capture_output=True, text=True)

        # If an error occurs during a step
        # Create an issue in GitHub and exit
        # Note: Something else is responsible for sending alerts to users based on issues
        # This script simply opens the issue
        if output.returncode != 0:
            print(output)
            stderr = output.stderr
            stdout = output.stdout

            subprocess.run(["gh", "issue", "create", "--label", "e2e test failed", "--title", f"Failed on step: {step}", "--body", f"The end to end test script failed on step: {step}\n\n## Error\n```\n{output.stderr}\n```\n\n## Output\n```\n{output.stdout}\n```"])
            exit(0)