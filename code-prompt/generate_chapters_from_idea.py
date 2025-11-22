import json
from pathlib import Path

from ai_utils import normalize_to_english, call_gemini_text

STORY_IDEA_FILE = Path("story_idea.txt")
CHAPTERS_FILE = Path("chapters.txt")


def load_story_idea() -> str:
    if not STORY_IDEA_FILE.exists():
        raise FileNotFoundError(
            "Không tìm thấy story_idea.txt. Hãy chạy B0/B1 để tạo file trước."
        )
    return STORY_IDEA_FILE.read_text(encoding="utf-8").strip()


def save_chapters(text: str):
    CHAPTERS_FILE.write_text(text, encoding="utf-8")


def build_prompt_for_chapters(story_idea_en: str) -> str:
    """
    Prompt yêu cầu Gemini sinh CHAPTER, luôn trả về tiếng Anh.
    Bạn có thể chỉnh sửa thêm tone, style ở đây nếu muốn.
    """

    prompt = f"""
You are a professional screenwriter and story-structure expert.

The following is a story idea for a film project. It is ALREADY IN ENGLISH.
Your tasks:

1. Understand the story idea and its three-act structure.
2. Break the story into numbered CHAPTERS (like beats or major sequences).
3. Each chapter should have:
   - a clear title
   - 2–5 sentences describing what happens in that chapter
   - focus on character goals, conflict, stakes, and emotional turns.
4. Output MUST be in ENGLISH ONLY.
5. Format: one JSON object per line, each with:
   {{
     "chapter_number": 1,
     "chapter_title": "...",
     "chapter_summary": "2-5 sentences in English...",
     "focus_characters": ["LANA", "ADAI"],
     "approx_scenes": 3
   }}

6. The 'approx_scenes' field is your rough guess of how many scenes
   this chapter will contain later (we will use it to decide total scenes).

STORY IDEA (ENGLISH):
====================
{story_idea_en}
====================

Now output ONLY JSONL (one JSON object per line). Do not add explanations.
"""
    return prompt


def main():
    print("📘 B2 – Generate CHAPTERS from story_idea.txt (normalize to EN)...")

    # 1) Đọc story_idea (có thể Việt / Anh / mix)
    raw_idea = load_story_idea()
    if not raw_idea:
        raise ValueError("story_idea.txt đang trống.")

    # 2) Chuẩn hoá sang tiếng Anh (dùng Gemini)
    print("🔁 Đang chuẩn hoá story_idea thành tiếng Anh...")
    story_idea_en = normalize_to_english(raw_idea)

    # (optional) Lưu lại luôn bản EN (nếu bạn muốn giữ)
    Path("story_idea_en.txt").write_text(story_idea_en, encoding="utf-8")

    # 3) Gọi Gemini sinh chapters (EN only)
    prompt = build_prompt_for_chapters(story_idea_en)
    print("🤖 Đang gọi Gemini để sinh CHAPTERS (EN)...")
    chapters_text = call_gemini_text(prompt)

    # 4) Lưu file
    save_chapters(chapters_text)
    print(f"✅ Đã lưu chapters.txt (EN) – {CHAPTERS_FILE.resolve()}")


if __name__ == "__main__":
    main()
