# generate_chapters.py
# B3 – Tạo CHAPTERS từ STORY LOCK-IN (công thức 6 phần + 3 Quy tắc vàng)

from pathlib import Path
import sys
from ai_utils import call_gemini_text

BASE_DIR = Path(__file__).resolve().parent
STORY_LOCK_IN_FILE = BASE_DIR / "story_lock_in.txt"
OUTPUT_CHAPTERS_FILE = BASE_DIR / "chapters_editable.txt"

# Nếu trong ai_utils bạn có dùng model_name riêng thì có thể truyền qua system_prompt hoặc chỉnh ở đó.
SYSTEM_PROMPT = (
    "You are an expert Hollywood series writer and story architect. "
    "You generate episode chapters for a serialized story based strictly on the STORY LOCK-IN. "
    "You MUST follow the 6-part episode structure and the 3 GOLDEN RULES: "
    "1) Every episode MUST have one clear MISSION. "
    "2) Act 2 MUST contain a meaningful TWIST. "
    "3) Act 3 MUST deliver the PEAK MOMENT of the episode. "
    "Output must follow exactly the chapter template provided by the user. "
    "Return text only, no extra explanations."
)

CHAPTER_USER_PROMPT_TEMPLATE = """
Below is the STORY LOCK-IN of the project.
Generate the full list of CHAPTERS (episodes) for the entire season, in Vietnamese where appropriate (labels can remain English if needed).

========================
STORY LOCK-IN:
{story_lock_in_text}
========================

Your task:
Create all chapters (episodes) for the season, following:

========================
CHAPTER OUTPUT TEMPLATE
========================

=== CHAPTER X: [Title of Episode] ===

1. MISSION (Nhiệm vụ chính)
- One clear and concise mission for the episode.

2. COLD OPEN (Cảnh mở đầu gây sốc)
- 2–4 sentences that immediately hook the audience.

3. ACT 1 – SETUP (Khởi đầu)
- Introduce conflict, environment, and characters' starting position.

4. ACT 2 – CONFLICT + TWIST (Xung đột + Twist)
- Rising obstacles.
- MUST include a significant TWIST that changes the direction of the mission.

5. ACT 3 – CLIMAX (Đỉnh điểm của tập)
- The most intense and emotional moment.
- A decisive battle, confrontation, escape, reveal, or sacrifice.

6. ACT 4 – RESOLUTION (Dư âm)
- Aftermath of the climax.
- Consequences or emotional fallout.

7. CLIFFHANGER (Cài bẫy tập sau)
- End the episode with a dramatic hook.

8. EPISODE MEANING / MESSAGE (Ý nghĩa / thông điệp của tập)
- A short sentence explaining the lesson or message of the episode.
  (Example: “Perseverance matters more than raw strength.”)
- This field is editable later by the user.

9. DESIRED SCENE COUNT (Số lượng SCENE cho tập này)
- Put exactly one line:
>>> [enter number here]
- Leave it as a placeholder so that the user can edit later.
  (Do NOT guess a number. Just keep the placeholder.)

10. NOTES (Ghi chú)
- 1–3 bullet points.
- Used for continuity (recurring characters, world rules, foreshadowing, etc.)

========================
RULES TO FOLLOW
========================
- Every episode MUST use all 10 sections exactly as stated.
- Episodes MUST follow the world rules from the Story Lock-In.
- Episode count must match the season plan in the Story Lock-In (if provided).
- Each episode must strongly relate to the CORE MISSION of the season.
- Keep content cinematic, coherent, and not repetitive.
- Return ONLY the chapters in correct template.
- Do NOT wrap everything in JSON, only plain text with headings.

Now generate ALL CHAPTERS.
"""


def main():
    print("🎬 B3 – Tạo CHAPTERS từ STORY LOCK-IN (story_lock_in.txt)")
    print("---------------------------------------------------------")

    if not STORY_LOCK_IN_FILE.exists():
        print(f"❌ Không tìm thấy file {STORY_LOCK_IN_FILE.name}.")
        print("➡ Hãy chạy B2 (generate_story_lock_in.py) và/hoặc chỉnh sửa story_lock_in.txt trước.")
        sys.exit(1)

    story_lock_in_text = STORY_LOCK_IN_FILE.read_text(encoding="utf-8").strip()
    if not story_lock_in_text:
        print("❌ File story_lock_in.txt đang trống.")
        print("➡ Hãy điền nội dung STORY LOCK-IN (B2) trước khi tạo CHAPTERS.")
        sys.exit(1)

    print(f"📖 Đã đọc STORY LOCK-IN từ {STORY_LOCK_IN_FILE.name} (độ dài {len(story_lock_in_text)} ký tự).")
    print("🧠 Đang gọi AI để sinh danh sách CHAPTERS theo công thức 6 phần + 3 Quy tắc vàng...")
    print("   (Tuỳ dung lượng, bước này có thể mất vài giây.)")

    user_prompt = CHAPTER_USER_PROMPT_TEMPLATE.format(
        story_lock_in_text=story_lock_in_text
    )

    try:
        ai_output = call_gemini_text(
            prompt=user_prompt,
            system_prompt=SYSTEM_PROMPT,
            max_output_tokens=4096,
        )
    except Exception as e:
        print("❌ Lỗi khi gọi AI để tạo CHAPTERS.")
        print(f"Chi tiết lỗi: {e}")
        sys.exit(1)

    ai_output = (ai_output or "").strip()
    if not ai_output:
        print("❌ AI trả về nội dung rỗng. Không thể tạo chapters_editable.txt.")
        sys.exit(1)

    OUTPUT_CHAPTERS_FILE.write_text(ai_output, encoding="utf-8")
    print(f"✅ Đã ghi danh sách CHAPTERS (editable) vào: {OUTPUT_CHAPTERS_FILE.name}")
    print("➡ Bạn có thể mở file này, chỉnh sửa từng tập, chỉnh mission / twist / climax / message / scene count tùy ý.")
    print("➡ Sau đó, bước tiếp theo (B4) sẽ tạo SCENES dựa trên nội dung và DESIRED SCENE COUNT của từng tập.")


if __name__ == "__main__":
    main()
