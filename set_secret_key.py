import secrets
import os

# Write a random urlsafe code to /tmp/secret

with open(file=f"/tmp/secret", mode="w") as secret_file:
    secret_file.write(secrets.token_urlsafe(8))