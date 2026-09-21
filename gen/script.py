from pathlib import Path
import os
import json
import re

soul = Path(os.getenv("SOUL_PROMPT_PATH")).read_text(encoding="utf-8")
script_prompt = Path(os.getenv("SCRIPT_PROMPT_PATH")).read_text(encoding="utf-8")

def gen_script(client, dryish_run:bool=True):
    content = [
        {"type": "text", "text": "Here is who you are: " + soul},
        {"type": "text", "text": "Now generate your script: " + script_prompt},
    ]
    if dryish_run:
        content.append({"type": "text", "text": "You should limit your script to a single very short story beat for testing purposes."})
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )
    return response.content[0].text

def correct_json(client, prev):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "This text is malformed json:" + prev},
                    {"type": "text", "text": "Please correct the json formatting while retaining the existing content as much as possible."},
                    {"type": "text", "text": "Do not include the json fence."},
                ]
            }
        ],
    )
    return response.content[0].text

def validate_script(client, script, dryish_run:bool=True):
    for _ in range(int(os.getenv("MAX_SCRIPT_RETRIES"))):
        try:
            json.loads(script)
            print("Script is valid json")
            return script
        except Exception as e:
            print("Script is not valid json. Trying to strip fence.")
            script = script.strip()
            script = re.sub(r'^```(?:json)?\s*', '', script)
            script = re.sub(r'\s*```$', '', script)
            try:
                json.loads(script)
                print("Script is valid json after stripping fence")
                return script
            except:
                print("Script is still invalid after stripping fence. Attempting corrections.")
                script = correct_json(client, script)
                try:
                    json.loads(script)
                    print("Script is valid json after correcting")
                    return script
                except:
                    pass