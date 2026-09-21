from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv(".env")
client = Anthropic()
SCRIPT_PROMPT_PATH = "prompts/script.md"
SOUL_PROMPT_PATH = "prompts/soul.md"

soul = Path(SOUL_PROMPT_PATH).read_text(encoding="utf-8")
gen_script = Path(SCRIPT_PROMPT_PATH).read_text(encoding="utf-8")

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Here is who you are: " + soul},
                {"type": "text", "text": "Now generate today's script: " + gen_script},
            ],
        }
    ],
)

print(response.content[0].text)
