# generate_scenes_from_chapters.py
# B4 – Tạo SCENES từ CHAPTERS (chapters_editable.txt)
#
# Pipeline:
# B3: chapters_editable.txt (mỗi CHAPTER có Mission, 4 Acts, Cold Open, Cliffhanger,
#                            Episode Meaning, Desired Scene Count, Notes)
#   ↓
# B4: scenes.txt (mỗi dòng = 1 cảnh mô tả thô, dùng cho generate_prompts.py)
#
# Mục tiêu:
# - Đọc từng CHAPTER block
# - Lấy DESIRED SCENE COUNT (nếu user đã sửa, vd: 8, 12, 100...)
# - Gọi AI sinh ra đúng số cảnh cho mỗi tập
# - Mỗi cảnh chỉ 1 dòng: "CHx-Sy: mô tả cảnh..."
# - scenes.txt = tất cả cảnh của mọi tập, mỗi cảnh 1 dòng (generate_prompts.py dùng tiếp)

from pathlib import Path
import re
import sys
import io
from ai_utils import call_gemini_text

# Fix Unicode encoding on Windows console
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
CHAPTERS_FILE = BASE_DIR / "chapters_editable.txt"
SCENES_FILE = BASE_DIR / "scenes.txt"

# Có thể chỉnh lại nếu muốn nhiều/ít cảnh khi không parse được số từ DESIRED SCENE COUNT
DEFAULT_SCENE_COUNT = 10

SYSTEM_PROMPT = (
    "You are a professional storyboard artist and screenwriter. "
    "You receive one episode chapter outline (MISSION, COLD OPEN, ACT 1–4, CLIFFHANGER, EPISODE MEANING). "
    "Your job is to break it down into a sequence of visual scenes. "
    "Each SCENE must be one line of text, no internal line breaks. "
    "Each line should start with a scene index and a short tag, then a concise but cinematic description. "
    "You MUST respect the requested scene count. "
    "Output only plain text lines, no extra commentary, no JSON."
)

USER_PROMPT_TEMPLATE = """
Below is the outline for one episode (chapter) in a serialized story.

========================
CHAPTER OUTLINE:
{chapter_block}
========================

Your task:
- Break this chapter into EXACTLY {scene_count} SCENES.
- Each scene should be concise (1–2 sentences) but cinematic and visual.
- Scenes must collectively cover:
  • Cold Open
  • Act 1 – Setup
  • Act 2 – Conflict + TWIST
  • Act 3 – CLIMAX (peak moment)
  • Act 4 – Resolution
  • Cliffhanger
- Respect the episode's mission and meaning/message.
- Ensure logical continuity from scene to scene.

OUTPUT FORMAT (VERY IMPORTANT):
- Output EXACTLY {scene_count} lines.
- Each line MUST represent ONE scene.
- NO empty lines.
- NO explanations above or below.
- Format for each line:
  CH{chapter_index}-S{scene_index}: [short visual scene description]

Examples of line style:
  CH1-S1: Cold open – at dawn, Sinbad wakes up to a thunderous roar as the cave shakes around him.
  CH1-S2: The crew rushes outside and sees a colossal one-eyed giant looming at the cliff's edge.

Do NOT wrap the output in JSON, lists, or bullet points.
Just raw lines, one per scene, nothing else.
"""


def split_chapters(raw_text: str):
    """
    Tách nội dung chapters_editable.txt thành các block CHAPTER riêng.
    Mỗi block bắt đầu bằng dòng: '=== CHAPTER ... ==='
    Trả về list các tuple (chapter_index, chapter_block_text).
    """
    lines = raw_text.splitlines()
    chapters = []
    current_block_lines = []
    current_index = None

    chapter_header_pattern = re.compile(r"^===\s*CHAPTER\s+(\d+)", re.IGNORECASE)

    for line in lines:
        header_match = chapter_header_pattern.match(line.strip())
        if header_match:
            # Nếu đang có block cũ thì push vào list
            if current_block_lines and current_index is not None:
                chapters.append((current_index, "\n".join(current_block_lines).strip()))
                current_block_lines = []

            # Bắt đầu block mới
            current_index = int(header_match.group(1))
            current_block_lines.append(line)
        else:
            if current_index is not None:
                current_block_lines.append(line)

    # Block cuối
    if current_block_lines and current_index is not None:
        chapters.append((current_index, "\n".join(current_block_lines).strip()))

    return chapters


def extract_scene_count_from_chapter(chapter_block: str) -> int:
    """
    Tìm DESIRED SCENE COUNT trong chapter_block.
    Expect format:
      9. DESIRED SCENE COUNT ...
      >>> 12
    hoặc:
      >>> 100
    Nếu không parse được, trả về DEFAULT_SCENE_COUNT.
    """
    # Tìm dòng có 'DESIRED SCENE COUNT'
    lines = chapter_block.splitlines()
    desired_line_index = None
    for idx, line in enumerate(lines):
        if "DESIRED SCENE COUNT" in line.upper():
            desired_line_index = idx
            break

    if desired_line_index is not None:
        # Tìm dòng tiếp theo có '>>>' hoặc chứa số
        for j in range(desired_line_index + 1, min(desired_line_index + 5, len(lines))):
            stripped = lines[j].strip()
            if not stripped:
                continue
            # Nếu dạng '>>> 12' hoặc '>>> [enter number here]'
            if stripped.startswith(">>>"):
                # Lấy phần sau '>>>'
                value = stripped[3:].strip()
                # Nếu user chưa sửa placeholder, value có thể là '[enter number here]'
                # Thử parse số từ value
                m = re.search(r"(\d+)", value)
                if m:
                    try:
                        return int(m.group(1))
                    except ValueError:
                        pass
            else:
                # Nếu không bắt đầu bằng >>>, vẫn thử parse số
                m = re.search(r"(\d+)", stripped)
                if m:
                    try:
                        return int(m.group(1))
                    except ValueError:
                        pass

    # Nếu không tìm được gì
    return DEFAULT_SCENE_COUNT


def main():
    print("🎬 B4 – Tạo SCENES từ CHAPTERS (chapters_editable.txt)")
    print("------------------------------------------------------")

    if not CHAPTERS_FILE.exists():
        print(f"❌ Không tìm thấy file {CHAPTERS_FILE.name}.")
        print("➡ Hãy chạy B3 (generate_chapters.py) và/hoặc chỉnh sửa chapters_editable.txt trước.")
        sys.exit(1)

    raw_chapters_text = CHAPTERS_FILE.read_text(encoding="utf-8").strip()
    if not raw_chapters_text:
        print("❌ File chapters_editable.txt đang trống.")
        print("➡ Hãy kiểm tra lại bước B3.")
        sys.exit(1)

    chapters = split_chapters(raw_chapters_text)
    if not chapters:
        print("❌ Không tách được CHAPTER nào từ chapters_editable.txt.")
        print("➡ Hãy kiểm tra format: mỗi chapter phải bắt đầu bằng dòng '=== CHAPTER X: ... ==='.")
        sys.exit(1)

    total_chapters = len(chapters)
    print(f"📖 Đã tìm thấy {total_chapters} CHAPTER trong {CHAPTERS_FILE.name}.")

    all_scene_lines = []

    for idx, (chapter_index, chapter_block) in enumerate(chapters, start=1):
        print(f"\n🔧 Đang xử lý CHAPTER {chapter_index} ({idx}/{total_chapters})...")

        scene_count = extract_scene_count_from_chapter(chapter_block)
        if scene_count == DEFAULT_SCENE_COUNT:
            print(f"⚠️ Không tìm thấy hoặc không parse được DESIRED SCENE COUNT, dùng mặc định: {DEFAULT_SCENE_COUNT} cảnh.")
        else:
            print(f"🎯 Số lượng cảnh yêu cầu cho CHAPTER {chapter_index}: {scene_count} cảnh.")

        user_prompt = USER_PROMPT_TEMPLATE.format(
            chapter_block=chapter_block,
            scene_count=scene_count,
            chapter_index=chapter_index,
        )

        try:
            scenes_text = call_gemini_text(
                user_prompt,
                system_instruction=SYSTEM_PROMPT
            )
        except Exception as e:
            print(f"❌ Lỗi khi gọi AI để tạo SCENES cho CHAPTER {chapter_index}.")
            print(f"Chi tiết lỗi: {e}")
            print("⛔ Bỏ qua CHAPTER này và tiếp tục CHAPTER tiếp theo.")
            continue

        scenes_text = (scenes_text or "").strip()
        if not scenes_text:
            print(f"❌ AI trả về nội dung rỗng cho CHAPTER {chapter_index}. Bỏ qua.")
            continue

        # Tách theo dòng – mỗi dòng = 1 scene
        scene_lines = [line.strip() for line in scenes_text.splitlines() if line.strip()]
        if len(scene_lines) != scene_count:
            print(
                f"⚠️ Số dòng scene AI trả về ({len(scene_lines)}) "
                f"không khớp scene_count yêu cầu ({scene_count}). Vẫn ghi toàn bộ."
            )

        # Ghi thêm comment nhẹ để biết thuộc CHAPTER nào? -> prefix đã có CHx-Sy
        all_scene_lines.extend(scene_lines)

    if not all_scene_lines:
        print("❌ Không có cảnh nào được tạo. Không ghi scenes.txt.")
        sys.exit(1)

    SCENES_FILE.write_text("\n".join(all_scene_lines) + "\n", encoding="utf-8")
    print(f"\n✅ Đã ghi {len(all_scene_lines)} cảnh vào: {SCENES_FILE.name}")
    print("➡ Bước tiếp theo: chạy generate_prompts.py để tạo prompt từ scenes.txt.")
    print("   (Mỗi dòng trong scenes.txt là một scene mô tả thô – dạng text.)")


if __name__ == "__main__":
    main()
