# generate_chapters_from_idea.py

import google.generativeai as gen
from pathlib import Path

API_KEYS_FILE = "api_keys.txt"
IDEA_FILE = "story_idea.txt"
CHAPTERS_FILE = "chapters.txt"

# Bạn có thể chỉnh nếu muốn khoảng chương khác
TARGET_MIN_CHAPTERS = 6
TARGET_MAX_CHAPTERS = 12


def load_api_keys(path: str = API_KEYS_FILE):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Không tìm thấy {path}")

    keys = [
        line.strip()
        for line in p.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not keys:
        raise ValueError("❌ Không tìm thấy API key nào trong api_keys.txt")

    print(f"🔑 Đã nạp {len(keys)} API key.")
    return keys


API_KEYS = load_api_keys()
current_key_index = 0


def set_current_key():
    gen.configure(api_key=API_KEYS[current_key_index])
    print(f"🔑 Đang dùng API key #{current_key_index + 1}")


set_current_key()


def switch_key():
    global current_key_index
    current_key_index = (current_key_index + 1) % len(API_KEYS)
    set_current_key()


CHAPTER_PROMPT_TEMPLATE = """
You are a professional story architect and mythic storyteller.

INPUT:
The user gives you a high-level idea for a story, including:
- World / setting
- Main characters
- 3-act structure (beginning, middle, end) or equivalent
- Optional preference for number of chapters

YOUR TASK:
1. Read and understand the idea and structure.
2. Create a complete STORY OUTLINE divided into CHAPTERS.
3. Aim for between {min_chapters} and {max_chapters} chapters total,
   UNLESS the user explicitly requests a specific number of chapters
   in the idea text (then respect that).
4. Each CHAPTER must have:
   - A short title (1 line)
   - A short summary (2–4 sentences) describing the key events in that chapter.
5. The outline must feel like a mythic/fantasy or cinematic story,
   with clear progression, escalation, and climax.
6. All text must be in NATURAL ENGLISH.

STRICT OUTPUT FORMAT:
Use ONLY this exact format, with blank lines between chapters:

CHAPTER 1: [Chapter 1 title]
[2–4 sentences summary]

CHAPTER 2: [Chapter 2 title]
[2–4 sentences summary]

CHAPTER 3: [Chapter 3 title]
[2–4 sentences summary]

...
(do not add any commentary before or after)

Do NOT write JSON.
Do NOT number scenes here, only chapters.

USER IDEA:
\"\"\"{idea_text}\"\"\"
"""


def call_gemini(prompt: str) -> str:
    """
    Gọi Gemini sinh outline CHAPTERS, tự xoay API key nếu lỗi.
    """
    global current_key_index

    for _ in range(len(API_KEYS)):
        try:
            model = gen.GenerativeModel("models/gemini-2.5-flash")
            resp = model.generate_content(prompt)
            text = (resp.text or "").strip()

            if text.startswith("```"):
                text = text.replace("```", "").strip()

            return text

        except Exception as e:
            print(f"⚠️ Lỗi với key #{current_key_index + 1}: {e}")
            print("🔄 Đổi sang API key tiếp theo...")
            switch_key()

    raise Exception("❌ Tất cả API key đều lỗi hoặc hết quota khi sinh CHAPTERS.")


def main():
    idea_path = Path(IDEA_FILE)
    if not idea_path.exists():
        print(f"❌ Không tìm thấy {IDEA_FILE}. Hãy tạo file này và mô tả ý tưởng vào.")
        return

    idea_text = idea_path.read_text(encoding="utf-8").strip()
    if not idea_text:
        print(f"❌ File {IDEA_FILE} đang trống.")
        return

    prompt = CHAPTER_PROMPT_TEMPLATE.format(
        min_chapters=TARGET_MIN_CHAPTERS,
        max_chapters=TARGET_MAX_CHAPTERS,
        idea_text=idea_text,
    )

    print("⏳ Đang sinh outline CHAPTERS từ ý tưởng...")
    chapters_text = call_gemini(prompt)

    out_path = Path(CHAPTERS_FILE)
    out_path.write_text(chapters_text, encoding="utf-8")

    print(f"✅ Đã sinh outline chương và lưu vào {CHAPTERS_FILE}")


if __name__ == "__main__":
    main()
