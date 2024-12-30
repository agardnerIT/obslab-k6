from fastapi import FastAPI
from pydantic import BaseModel # For POST bodies
from fastapi.middleware.cors import CORSMiddleware # For localhost CORS access
from loguru import logger
import subprocess
import json
import re
import os
from ansi2html import Ansi2HTMLConverter

with open("/tmp/secret", mode="r") as secret_file:
    SECRET_KEY = secret_file.readline()
    SECRET_KEY = SECRET_KEY.strip()

if SECRET_KEY == "":
    logger.error("SECRET_KEY is empty. Investigate. Exiting.")
    exit()
#
# {"filename": "install.md", "command": "kind delete cluster", "secret_key": "xxxxx"}
#
class RequestBody(BaseModel):
    filename: str
    snippet_id: str
    secret_key: str | None = ""

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# When a user retrieves the
# secret key from /tmp/secret
# The shell has an annoying habit of putting `%` at the end
# So rather than asking hte user to chop it off
# We just chop it off for them (if it is present)
def sanitise_secret_key(secret_key):
    if secret_key.endswith("%"):
        secret_key = secret_key[:-1]
    return secret_key

# Takes any string and:
# 1. Converts to lowercase
# 2. Removes all non-alphanumeric characters
# 3. Gets the first two words
# 4. Joins them with a hyphen
# def clean_string(text):
#     # Convert to lowercase
#     text = text.lower()
#     # Keep only alphanumeric chars, spaces and dashes
#     text = re.sub(r'[^a-z0-9-\s]', '', text)
#     # Split into words and take first two
#     words = text.split()[:2]

#     # words should always be 2 long
#     # otherwise something went wrong
#     if len(words) != 2:
#         logger.error("words was not 2 long. Investigate.")
#         return ""

#     # Special rule
#     # If either word starts of ends with hyphen
#     # just smush them together
#     # otherwise add a hyphen
#     # Why? Without this special case:
#     # ["ls", "-al"] becomes "ls--al" which isn't correct
#     # it should be "ls-al"

#     if words[0].startswith("-") or words[0].endswith("-") or words[1].startswith("-") or words[1].endswith("-"):
#        return ''.join(words)
#     else:
#         # Join with hyphen
#         return '-'.join(words)

@app.post("/query")
def execute_query(body: RequestBody):

    # If incoming secret doesn't match system secret
    # exit immediately

    secret_key_input = sanitise_secret_key(body.secret_key)

    if secret_key_input != SECRET_KEY:
        logger.error("invalid secret key")
        return {
            "return_code": -1,
            "output": format_text("Invalid secret key. Please check and try again.")
        }
    
    snippet_id_to_execute = ""
    
    # First get the available snippets for this file
    # This is used to validate the incoming, user-provided input
    # filename is optional
    if body.filename != "":
        ls_output = subprocess.run(["runme", "--filename", body.filename, "ls", "--json"], capture_output=True, text=True)
    else: # Just get all snippets that runme can find
        ls_output = subprocess.run(["runme", "ls", "--json"], capture_output=True, text=True)

    # Something went wrong, probably a missing file
    # exit
    if ls_output.returncode != 0:
        logger.error(f"output of listing filename: {body.filename} caused an error.")
        return {
            "return_code": -1,
            "output": format_text(f"output of listing filename: {body.filename} caused an error.")
        }
    
    # Snippet naming logic is the first two strings (alphanumeric only) of the first list with space replaced by a dash
    # lowercased
    # eg.
    # ```
    # kind delete cluster 
    # ```
    # Becomes `name: kind-delete`
    # and
    # ```
    # a F1453%dj b 2 c 3 foo
    # ```
    # Becomes `name: a-1`
    #
    #
    # Lookup the correct snippet name
    # In the `input` field a user can provide either:
    # The snippet `name` OR the `first_command`
    # This logic prioritises the `name` first and falls back to `first_command`
    # Eg. Given two snippets
    # ```
    # ls -al
    # ```
    # and
    # ```{name="list all"}
    # ls -al
    # ```
    # and an `input`: `list all`
    # The SECOND snippet would be executed
    #
    # However, with an `input`: `ls -al`
    # The second snippet WOULD NOT match
    # and thus the FIRST snippet would be executed
    valid_snippets = json.loads(ls_output.stdout)
    snippet_name_to_execute = ""

    for snippet in valid_snippets:

        if body.snippet_id == snippet["name"]:
            snippet_name_to_execute = snippet["name"]
            break
    
    # If the input snippet name
    # is invalid, exit immediately
    if snippet_name_to_execute == "":
        logger.error("could not find a valid snippet to execute")
        return {
            "return_code": -1,
            "output": format_text("Could not find a valid snippet to execute")
        }

    if body.filename != "":
        output = subprocess.run(["runme", "--filename", body.filename, "run", snippet_name_to_execute], capture_output=True, text=True)
    else: # Run from main list of snippets
        output = subprocess.run(["runme", "run", snippet_name_to_execute], capture_output=True, text=True)
        print(f"Raw stdout: {output.stdout}")
    
    return_obj = {
        "return_code": output.returncode,
        "output": format_text(output.stdout)
    }

    if output.returncode != 0:
        return_obj["output"] = f"stderr: {format_text(output.stderr)}"
        
        if output.stdout != "":
            return_obj["output"] += f" stdout: {format_text(output.stdout)}"

    return return_obj

# This formats terminal output into pretty HTML
def format_text(input):
    output = input
    output = output.replace('\t', '&nbsp;' * 8)
    
    conv = Ansi2HTMLConverter()
    output = conv.convert(output, full=False)

    return output