import subprocess

with open("steps.txt", mode="r") as steps_file:
    steps = steps_file.readlines()

    for step in steps:

        output = subprocess.run(["runme", "run", step.strip()], capture_output=True, text=True)
        print("-- Step Output --")
        print(output)
        if output.returncode != 0:
            print("ERROR! Command Failed! Create an issue!")
            subprocess.run(["gh", "issue", "create", "--label", "e2e test failed", "--title", f"Failed on step {step.strip()}", "--body", f"The end to end test script failed on step: {step.strip()} with error: {output.stderr}"])
            exit(0)