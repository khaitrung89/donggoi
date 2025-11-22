# ================================
# B1 – Tạo STORY IDEA từ STORY SEED
# ================================
#
# Đọc story_seed.txt  (B0)
# → Gửi cho Gemini với prompt chuẩn
# → Ghi ra story_idea.txt (B1)
#
# Lưu ý:
#   Hàm call_gemini_text trong ai_utils.py
#   phải có dạng: call_gemini_text(prompt: str, ...)
#   KHÔNG dùng system_prompt / user_prompt nữa.

import os
from pathlib import Path
from ai_utils import call_gemini_text

BASE_DIR = Path(__file__).resolve().parent
SEED_FILE = BASE_DIR / "story_seed.txt"
OUTPUT_FILE = BASE_DIR / "story_idea.txt"


SYSTEM_INSTRUCTIONS = """
You are a professional story architect and screenwriter.

From a compact STORY SEED, you will create a full STORY IDEA / BLUEPRINT
that will later be used to generate a series outline (chapters & scenes).

The STORY IDEA must include:

1) SERIES_TITLE
   - A short, powerful series title.

2) LOGLINE
   - 1–2 sentences that clearly define:
     • Protagonist
     • Goal
     • Main conflict
     • Stakes

3) WORLD & ERA
   - Where and when does the story happen?
   - What makes this world unique?

4) CORE PREMISE
   - What is the core situation or promise of the series?

5) MAIN CHARACTERS
   - For each important character:
     • Name
     • Role
     • Goal
     • Inner flaw or wound
     • Basic arc direction

6) TONE & STYLE
   - Emotional tone of the series (dark, hopeful, comedic, epic, etc.)
   - Visual / cinematic style, based on the seed info.

7) 3-ACT SERIES SPINE
   ACT 1 – Setup:
     - Status quo, inciting incident, first turning point.
   ACT 2 – Confrontation:
     - Escalation, mid-point, big setback, growing stakes.
   ACT 3 – Resolution:
     - Final confrontation, resolution, new status quo.

8) SEASON STRUCTURE
   - Expected number of episodes (from seed if available).
   - Short description of what each episode focuses on (1–3 lines each).

9) THEMES & MESSAGE
   - Key themes (friendship, sacrifice, power, destiny, etc.)
   - Core message of the story in 1–3 sentences.

Output should be in clear sections with UPPERCASE headings,
easy to read and easy to edit by a human writer.
Do NOT use JSON. Use clean, human-readable text.
"""


def build_prompt(seed_text: str) -> str:
    return f"""{SYSTEM_INSTRUCTIONS}

========================
RAW STORY SEED (B0):
========================
{seed_text}

========================
TASK:
========================
Based on the STORY SEED above, write a complete STORY IDEA / BLUEPRINT
following the structure in the instructions.
"""


def main():
    print("📝 B1 – Tạo STORY IDEA (story_idea.txt) từ STORY SEED (story_seed.txt)")
    print("--------------------------------------------------------------------")

    if not SEED_FILE.exists():
        print(f"❌ Không tìm thấy {SEED_FILE.name}. Hãy chạy B0 và lưu story_seed.txt trước.")
        return

    seed_text = SEED_FILE.read_text(encoding="utf-8").strip()
    if not seed_text:
        print(f"❌ File {SEED_FILE.name} đang rỗng. Hãy điền nội dung B0 trước.")
        return

    print(f"📖 Đã đọc STORY SEED từ {SEED_FILE.name} (độ dài {len(seed_text)} ký tự).")
    print("🧠 Đang gọi AI để sinh STORY IDEA (B1)...")
    print("   (Bước này có thể mất vài giây tuỳ độ dài seed.)")

    try:
        prompt = build_prompt(seed_text)
        story_idea = call_gemini_text(prompt)  # ✅ dùng đúng signature mới
    except Exception as e:
        print("❌ Lỗi khi gọi AI để tạo STORY IDEA (B1).")
        print("Chi tiết lỗi:", e)
        return

    if not story_idea or len(story_idea.strip()) < 50:
        print("❌ Kết quả AI trả về quá ngắn hoặc rỗng. Kiểm tra lại API key / quota.")
        return

    OUTPUT_FILE.write_text(story_idea.strip(), encoding="utf-8")
    print(f"✅ Đã ghi STORY IDEA vào {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
