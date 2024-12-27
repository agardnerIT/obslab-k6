import subprocess

with open("steps.txt", mode="r") as steps_file:
    steps = steps_file.readlines()

    for step in steps:

        output = subprocess.run(["runme", "run", step.strip()], capture_output=True, text=True)

        # If an error occurs during a step
        # Create an issue in GitHub and exit
        # Note: Something else is responsible for sending alerts to users based on issues
        # This script simply opens the issue
        if output.returncode != 0:
            subprocess.run(["gh", "issue", "create", "--label", "e2e test failed", "--title", f"Failed on step: {step.strip()}", "--body", f"The end to end test script failed on step: {step.strip()} with error: {output.stderr}"])
            exit(0)