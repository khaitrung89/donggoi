import os
import sys
import io
from pathlib import Path
from ai_utils import call_gemini_text

# Fix Unicode encoding on Windows console
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

INPUT_FILE = "story_idea.txt"
OUTPUT_FILE = "story_lock_in.txt"

SYSTEM_PROMPT = """
You are an expert story architect.
Your task is to convert the user's STORY IDEA into a STORY LOCK-IN document.

STORY LOCK-IN must contain:

1) WORLD OVERVIEW (core rules)
2) MAIN CAST (3–8 characters, each 1–2 lines)
3) SEASON ARC (overall conflict)
4) THEMES (core meanings)
5) EPISODE STRUCTURE (6-Part Formula + 3 Golden Rules)
6) FINAL LOCK-IN SUMMARY (the foundation for generating chapters later)

Write all content in English.
Clear, structured, no rambling.
"""

USER_PROMPT_TEMPLATE = """
Convert the following STORY IDEA into a full STORY LOCK-IN.

STORY IDEA:
----------------
{story_idea}
----------------

Write the final LOCK-IN now.
"""


def read_file(path: str) -> str:
    if not os.path.exists(path):
        return None
    return Path(path).read_text(encoding="utf-8")


def write_file(path: str, text: str):
    Path(path).write_text(text, encoding="utf-8")


def generate_lock_in(story_idea: str) -> str:
    user_prompt = USER_PROMPT_TEMPLATE.format(story_idea=story_idea)
    response = call_gemini_text(
        user_prompt,
        system_instruction=SYSTEM_PROMPT
    )
    return response


def main():
    print("B2 – Generating STORY LOCK-IN...")

    story_idea = read_file(INPUT_FILE)

    if story_idea is None:
        print(f"[ERROR] Cannot find {INPUT_FILE}. Make sure B1 has been generated.")
        return

    lock_in = generate_lock_in(story_idea)
    write_file(OUTPUT_FILE, lock_in)

    print(f"[OK] STORY LOCK-IN generated → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
