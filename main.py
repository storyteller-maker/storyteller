from dotenv import load_dotenv
print("Loading environment")
load_dotenv(".env")

from anthropic import Anthropic
from gen.script import gen_script, correct_json, validate_script
import os

client = Anthropic()

print("Generating script")
script = gen_script(client)

print("Validating script")
script = validate_script(client, script)
if not script:
    raise Exception("Failed to produce a valid script.")