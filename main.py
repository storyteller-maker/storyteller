from pathlib import Path
from anthropic import Anthropic

client = Anthropic()
SCRIPT_PROMPT_PATH = "prompts/script.md"

def generate_video_script():
    content = Path(SCRIPT_PROMPT_PATH).read_text(encoding="utf-8")
    
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Here is the memory file:\n\n" + script_content},
                    {"type": "text", "text": "Now generate today's script."},
                ],
            }
        ],
    )

def main():
    # call claude to generate script
    script = generate_video_script()
