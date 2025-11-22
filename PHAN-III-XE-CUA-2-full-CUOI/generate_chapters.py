# generate_chapters.py
# B3 – Tạo CHAPTERS từ STORY LOCK-IN (B2)
#
# Pipeline:
# B2: story_lock_in.txt   (đã khóa cốt truyện, core conflict, theme, engine...)
#   +
# (optional) story_seed.txt (EPISODES, SCENES_PER_EP)
#   ↓
# B3: chapters_editable.txt
#
# Mỗi CHAPTER = 1 tập phim với cấu trúc:
# - Cold Open
# - Act 1
# - Act 2 (có TWIST bắt buộc)
# - Act 3 (đỉnh nhất của tập)
# - Act 4
# - Cliffhanger
#
# Và 3 QUY TẮC VÀNG:
# 1) Mỗi tập phải có 1 nhiệm vụ rõ ràng (EPISODE MISSION)
# 2) Act 2 LUÔN có TWIST
# 3) Act 3 phải có khoảnh khắc "đỉnh nhất của tập"
#
# Đồng thời có:
# - EPISODE MEANING (MESSAGE)
# - DESIRED SCENE COUNT (số cảnh mong muốn – dùng cho B4)
# - NOTES (để bạn chỉnh tay)
#
# Kết quả: chapters_editable.txt
#   → B4 generate_scenes_from_chapters.py sẽ đọc file này.

import re
import sys
import io
from pathlib import Path
from ai_utils import call_gemini_text

# Fix Unicode encoding on Windows console
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
LOCKIN_FILE = BASE_DIR / "story_lock_in.txt"
SEED_FILE = BASE_DIR / "story_seed.txt"
CHAPTERS_FILE = BASE_DIR / "chapters_editable.txt"

# Default nếu không lấy được từ seed
DEFAULT_EPISODES = 10
DEFAULT_SCENES_PER_EP = 20

SYSTEM_PROMPT = (
    "You are a senior TV series writer and story architect. "
    "Your job is to take a STORY LOCK-IN document and break it into a season outline with episodes. "
    "Each episode must be structured for screenwriting and later broken into SCENES. "
    "Follow the required template and structure exactly, using clear headings and sections. "
    "Use cinematic tone and concise but vivid descriptions."
)

USER_PROMPT_TEMPLATE = """
We are creating a serialized story for a season.

You are given a STORY LOCK-IN (B2) that contains:
- Core conflict
- Season engine
- Theme & tone
- Character arcs
- Golden triangle (conflict, stakes, consequence)
- Episode-arc overview guidelines

========================
STORY LOCK-IN (INPUT):
========================
{lockin}
========================

We also have an initial desired structure:

- Total episodes (approx): {episodes}
- Approx scenes per episode: {scenes_per_ep}

Your task:
Create a complete season chapter outline where EACH EPISODE becomes ONE CHAPTER, following this strict template.

========================
REQUIRED OUTPUT FORMAT:
========================

For each episode i (starting from 1), output the following block:

=== CHAPTER i: [EPISODE TITLE HERE] ===

1. EPISODE TITLE
>>> [short, punchy title – cinematic, 2–6 words]

2. EPISODE MISSION (clear goal of the episode)
>>> [1–3 sentences. Very clear mission. No mission = no episode.]

3. COLD OPEN – shocking / hook intro
>>> [2–5 sentences – must hook the viewer, create curiosity.]

4. ACT 1 – Set-up for this episode
>>> [4–8 sentences – introduce the problem of THIS episode, connect to the season conflict.]

5. ACT 2 – Rising conflict + TWIST (MANDATORY)
>>> [5–10 sentences – escalate conflict, introduce obstacles, and MUST contain a clear TWIST moment.]

6. ACT 3 – CLIMAX (peak moment of the episode)
>>> [5–10 sentences – the most intense moment of THIS episode, emotional or action peak.]

7. ACT 4 – Resolution + emotional aftermath
>>> [4–8 sentences – partial resolution, emotional consequences, but do not destroy the overall season tension.]

8. CLIFFHANGER – hook into next episode
>>> [2–5 sentences – clear hook for the next episode, a new reveal, or a new danger.]

9. EPISODE MEANING (MESSAGE)
>>> [1–3 sentences – what emotional/ethical idea this episode leaves the viewer with.]

10. DESIRED SCENE COUNT
>>> {scenes_per_ep}

11. NOTES
>>> [optional writer notes: which character arcs progress here, any motifs, recurring symbols, etc.]

========================
RULES (VERY IMPORTANT):
========================

- Apply the **3 GOLDEN RULES** to EVERY episode:
  1) Each episode must have ONE clear MISSION. (EPISODE MISSION)
  2) ACT 2 MUST contain a TWIST (plot or character).
  3) ACT 3 MUST contain the PEAK MOMENT of the episode (why the viewer watches the whole episode).

- The season must:
  • Progress the CORE CONFLICT in every episode.
  • Escalate stakes gradually.
  • Develop character arcs in a meaningful way.
  • Keep enough tension for the finale.

- Use the EPISODE COUNT as a guideline. If the LOCK-IN strongly suggests a different structure, you may slightly adjust, but prefer to stick to the given episode count.

- Output format MUST be plain text, and MUST follow the exact headings and '>>>' markers as shown.
- Do NOT add any commentary outside of the CHAPTER blocks.
"""


def parse_seed_for_counts(seed_text: str):
    """
    Lấy EPISODES và SCENES_PER_EP từ story_seed.txt nếu có.
    Định dạng mong đợi:
      EPISODES: 10
      SCENES_PER_EP: 20
    Nếu không thấy, trả về default.
    """
    episodes = DEFAULT_EPISODES
    scenes_per_ep = DEFAULT_SCENES_PER_EP

    # EPISODES
    m_ep = re.search(r"EPISODES\s*:\s*(\d+)", seed_text, re.IGNORECASE)
    if m_ep:
        try:
            episodes = int(m_ep.group(1))
        except ValueError:
            pass

    # SCENES_PER_EP
    m_sc = re.search(r"SCENES_PER_EP\s*:\s*(\d+)", seed_text, re.IGNORECASE)
    if m_sc:
        try:
            scenes_per_ep = int(m_sc.group(1))
        except ValueError:
            pass

    return episodes, scenes_per_ep


def main():
    print("🎬 B3 – Tạo CHAPTERS từ STORY LOCK-IN (story_lock_in.txt)")
    print("----------------------------------------------------------")

    if not LOCKIN_FILE.exists():
        print(f"❌ Không tìm thấy {LOCKIN_FILE.name}. Hãy chạy B2 (generate_story_lock_in.py) trước.")
        return

    lockin_text = LOCKIN_FILE.read_text(encoding="utf-8").strip()
    if not lockin_text:
        print(f"❌ File {LOCKIN_FILE.name} đang trống. Hãy kiểm tra lại B2.")
        return

    # Đọc seed nếu có để lấy EPISODES & SCENES_PER_EP
    episodes = DEFAULT_EPISODES
    scenes_per_ep = DEFAULT_SCENES_PER_EP

    if SEED_FILE.exists():
        seed_text = SEED_FILE.read_text(encoding="utf-8")
        ep, sc = parse_seed_for_counts(seed_text)
        episodes, scenes_per_ep = ep, sc
        print(f"📌 Lấy từ story_seed.txt → EPISODES = {episodes}, SCENES_PER_EP = {scenes_per_ep}")
    else:
        print(f"⚠️ Không tìm thấy {SEED_FILE.name}, dùng mặc định EPISODES={episodes}, SCENES_PER_EP={scenes_per_ep}")

    user_prompt = USER_PROMPT_TEMPLATE.format(
        lockin=lockin_text,
        episodes=episodes,
        scenes_per_ep=scenes_per_ep,
    )

    print("🧠 Đang gọi AI để tạo outline CHAPTERS theo cấu trúc 6 phần + 3 quy tắc vàng...")
    try:
        chapters_text = call_gemini_text(
            user_prompt,
            system_instruction=SYSTEM_PROMPT
        )
    except Exception as e:
        print("❌ Lỗi khi gọi AI:", e)
        return

    if not chapters_text or len(chapters_text.strip()) < 50:
        print("❌ AI trả về nội dung quá ngắn hoặc rỗng. Có thể lỗi API key / quota.")
        return

    final_text = chapters_text.strip()

    # Ghi ra file để user có thể chỉnh tay
    CHAPTERS_FILE.write_text(final_text + "\n", encoding="utf-8")
    print(f"✅ Đã ghi outline {episodes} CHAPTER vào {CHAPTERS_FILE.name}")
    print("➡ Bạn có thể mở B3 trong GUI để chỉnh sửa thêm trước khi sang B4.")


if __name__ == "__main__":
    main()
