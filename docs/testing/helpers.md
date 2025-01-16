```sh {"name":"check env vars exist"}
if [ -z "${DT_URL}" ]; then
  exit 1
fi
if [ -z "${DT_K6_TOKEN}" ]; then
  exit 1
fi
```

```python {"name":"wait for docker to start"}
import subprocess
import time

output = subprocess.run(["docker", "ps"], capture_output=True, text=True)

SEARCHING_FOR_STRING = "CONTAINER ID"
CURRENT_TIME = 1
TIMEOUT = 30
STRING_FOUND = False

# Check first to avoid any redundant loops
if SEARCHING_FOR_STRING in output.stdout:
    STRING_FOUND = True

# String not found at first
# Let's give it some time for docker to start
# Loop for a max of 5 seconds OR until string is found (early exit)
while CURRENT_TIME < 30 and not STRING_FOUND:
    
    output = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    foo = output.stdout

    if SEARCHING_FOR_STRING in output.stdout:
        STRING_FOUND = True
        break

    CURRENT_TIME += 1
    time.sleep(1)

if STRING_FOUND:
    print(f"String found in {CURRENT_TIME}s")
else:
    print(f"String still not found after: {CURRENT_TIME}s")
```
