# generate_story_idea_from_seed.py
# B1 – Tạo STORY IDEA (story_idea.txt) từ B0 (story_seed.txt)
#
# Pipeline:
# B0: story_seed.txt (Ý tưởng + thể loại + phong cách)
#   ↓
# B1: story_idea.txt (bộ khung cốt truyện đầy đủ, người dùng có thể chỉnh sửa)
#   ↓
# B2: generate_story_lock_in.py
#   ↓
# B3: generate_chapters.py
#   ...

from pathlib import Path
import sys
from ai_utils import call_gemini_text

BASE_DIR = Path(__file__).resolve().parent
STORY_SEED_FILE = BASE_DIR / "story_seed.txt"
STORY_IDEA_FILE = BASE_DIR / "story_idea.txt"

SYSTEM_PROMPT = (
    "You are an expert story development writer for films and series. "
    "You receive a short story seed with an idea, genres, and style. "
    "Your job is to expand it into a structured STORY IDEA document (B1) "
    "that will later be used to build a serialized season. "
    "You MUST follow exactly the STORY IDEA TEMPLATE given by the user. "
    "Use natural Vietnamese for descriptions when the seed is Vietnamese, "
    "but keep the headings in the same language and format as the template. "
    "Return plain text only, no JSON."
)

USER_PROMPT_TEMPLATE = """
Dưới đây là STORY SEED (B0) của dự án:

========================
STORY SEED (B0)
========================
{story_seed_text}
========================

Nhiệm vụ của bạn:
Từ STORY SEED trên, hãy viết ra một tài liệu STORY IDEA hoàn chỉnh (B1),
theo đúng template sau:

========================
STORY IDEA TEMPLATE (B1)
========================

TITLE:
[Đặt một tiêu đề phim / dự án phù hợp với seed]

LOGLINE:
[Một câu logline tóm tắt xung đột chính của toàn câu chuyện]

WORLD_AND_SETTING:
[Mô tả thế giới, bối cảnh, thời đại, không khí chung.
Nêu rõ: thế giới hiện đại / tương lai / cổ trang / trung cổ / fantasy...
Mô tả 1–2 địa điểm chính và cảm giác hình ảnh.]

MAIN_AND_SUPPORTING_CHARACTERS:
[Mô tả các nhân vật quan trọng nhất.
Cho mỗi nhân vật: tên, vai trò (chính/phụ/đối kháng), tính cách, mục tiêu, điểm yếu.
Có thể viết dạng đoạn văn hoặc danh sách.]

THEME_AND_TONE:
[Mô tả chủ đề (theme) và tone cảm xúc của câu chuyện.
Ví dụ: tình bạn, hi sinh, nỗi sợ, đối mặt với quá khứ...
Nêu rõ: tone ấm áp / u tối / cảm động / căng thẳng...]

MEANING_MESSAGE:
[1–3 câu: câu chuyện muốn nói điều gì về con người/cuộc sống?
Ý nghĩa sâu xa nếu xem hết cả mùa phim.]

ACT_1_SETUP:
[Tóm tắt Act 1 – cách câu chuyện mở đầu:
nhân vật đang ở đâu, cuộc sống hiện tại, sự kiện mở đầu, biến cố khởi đầu (inciting incident).]

ACT_2_CONFRONTATION:
[Tóm tắt Act 2 – tuyến xung đột chính:
họ gặp những khó khăn gì, đối đầu với ai, thế giới mở rộng ra sao,
các mối quan hệ thay đổi như thế nào.]

ACT_3_RESOLUTION:
[Tóm tắt Act 3 – cao trào & kết của mùa:
đối đầu cuối cùng, bài học, sự thay đổi của nhân vật chính,
và thế giới được giải quyết đến mức nào (còn treo hay kết thúc hẳn).]

EXPECTED_CHAPTER_COUNT:
[Đề xuất số CHAPTER / tập hợp lý dựa trên loại câu chuyện (ví dụ: 8, 10, 12...).]

EXPECTED_SCENE_COUNT:
[Đề xuất số SCENE trung bình / một tập (ví dụ: 8–12).
Có thể ghi dạng: “8–12” hoặc một con số ước tính.]

========================
YÊU CẦU:
- Hãy TRỰC TIẾP điền nội dung vào các mục trong STORY IDEA TEMPLATE (B1).
- Giữ nguyên tiêu đề các mục (TITLE, LOGLINE, ...).
- Không thêm phần mục lạ ngoài template.
- Không trả về JSON, chỉ plain text theo template.
========================
"""


def main():
    print("📝 B1 – Tạo STORY IDEA (story_idea.txt) từ STORY SEED (story_seed.txt)")
    print("--------------------------------------------------------------------")

    if not STORY_SEED_FILE.exists():
        print(f"❌ Không tìm thấy file {STORY_SEED_FILE.name}.")
        print("➡ Hãy tạo file story_seed.txt với B0 (ý tưởng + thể loại + phong cách) trước.")
        sys.exit(1)

    story_seed_text = STORY_SEED_FILE.read_text(encoding="utf-8").strip()
    if not story_seed_text:
        print("❌ File story_seed.txt đang trống.")
        print("➡ Hãy điền ý tưởng & thể loại vào B0 trước.")
        sys.exit(1)

    print(f"📖 Đã đọc STORY SEED từ {STORY_SEED_FILE.name} (độ dài {len(story_seed_text)} ký tự).")
    print("🧠 Đang gọi AI để sinh STORY IDEA (B1)...")
    print("   (Bước này có thể mất vài giây tuỳ độ dài seed.)")

    user_prompt = USER_PROMPT_TEMPLATE.format(
        story_seed_text=story_seed_text
    )

    try:
        story_idea_text = call_gemini_text(
            prompt=user_prompt,
            system_prompt=SYSTEM_PROMPT,
            max_output_tokens=4096,
        )
    except Exception as e:
        print("❌ Lỗi khi gọi AI để tạo STORY IDEA (B1).")
        print(f"Chi tiết lỗi: {e}")
        sys.exit(1)

    story_idea_text = (story_idea_text or "").strip()
    if not story_idea_text:
        print("❌ AI trả về nội dung rỗng. Không thể tạo story_idea.txt.")
        sys.exit(1)

    STORY_IDEA_FILE.write_text(story_idea_text, encoding="utf-8")

    print(f"✅ Đã ghi STORY IDEA vào: {STORY_IDEA_FILE.name}")
    print("➡ Bạn có thể mở file này, chỉnh sửa thêm (thêm nhân vật, thay đổi Act...) nếu muốn.")
    print("➡ Sau đó chạy B2 (generate_story_lock_in.py) để khóa cốt truyện (STORY LOCK-IN).")


if __name__ == "__main__":
    main()
