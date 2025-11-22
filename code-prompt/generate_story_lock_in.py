# generate_story_lock_in.py
# B2 – Tạo STORY LOCK-IN từ story_idea.txt
#
# Mục tiêu:
# - Đọc B1 (story_idea.txt) = ý tưởng + thế giới + nhân vật + 3 hồi (do người dùng chỉnh sửa)
# - Gọi AI để sinh ra bản STORY LOCK-IN đầy đủ, có cấu trúc rõ ràng
# - File output: story_lock_in.txt
#
# B3 (generate_chapters.py) sẽ dùng file này để sinh các CHAPTER theo
# công thức 6 phần + 3 quy tắc vàng.

from pathlib import Path
import sys
from ai_utils import call_gemini_text

BASE_DIR = Path(__file__).resolve().parent
STORY_IDEA_FILE = BASE_DIR / "story_idea.txt"
STORY_LOCK_IN_FILE = BASE_DIR / "story_lock_in.txt"

SYSTEM_PROMPT = (
    "You are an expert Hollywood series writer and story architect. "
    "You receive a raw story idea file that may contain Vietnamese and English. "
    "Your job is to synthesize a clean, structured STORY LOCK-IN document for a serialized project. "
    "The STORY LOCK-IN will be used later to generate episodic chapters. "
    "You MUST strictly follow the STORY LOCK-IN template given by the user. "
    "Use Vietnamese for natural language prose (descriptions, explanations) when the source is Vietnamese, "
    "but keep the section headings in the same language and format as the template. "
    "Return plain text only, no JSON, no extra commentary."
)

USER_PROMPT_TEMPLATE = """
Dưới đây là nội dung story_idea.txt (B1),
bao gồm: ý tưởng, thế giới, nhân vật, 3 hồi... do người dùng chỉnh sửa.

========================
STORY IDEA (B1):
{story_idea_text}
========================

Nhiệm vụ của bạn:
Từ STORY IDEA trên, hãy tạo ra một tài liệu STORY LOCK-IN hoàn chỉnh cho toàn bộ dự án.
STORY LOCK-IN là bản “khóa cốt truyện” dùng để sinh ra các tập phim (chapters) sau này,
phải làm rõ:
- Cốt lõi câu chuyện (core story)
- Arc của cả mùa (season arc)
- Nhân vật chính / phản diện chính
- Chủ đề / thông điệp
- Engine vận hành series
- Mẫu cấu trúc 1 tập (episode template)
- Ghi chú ràng buộc cho bước tạo chương

Bạn PHẢI xuất kết quả theo đúng template dưới đây (giữ nguyên tiêu đề & thứ tự):

============================================================
STORY LOCK-IN TEMPLATE
============================================================

1. CORE STORY SUMMARY (TÓM TẮT CỐT LÕI)
- 1–2 đoạn ngắn:
  • Câu chuyện nói về ai?
  • Họ muốn gì? (Goal)
  • Họ sợ gì / yếu điểm? (Flaw/Fear)
  • Họ phải trả giá hoặc đấu tranh với điều gì?

2. REFINED LOGLINE (LOGLINE CHUẨN NHẤT)
- 1 câu, rõ:
  • Nhân vật chính
  • Mục tiêu
  • Thế lực / nguy cơ chính
  • Cái giá hoặc mâu thuẫn trung tâm

3. GENRE & STYLE RECAP (THỂ LOẠI & PHONG CÁCH)
- Genres: [...]
- Tone: [...]
- Visual style / Format: [...]

4. THEME & MESSAGE (CHỦ ĐỀ & Ý NGHĨA)
- Theme chính (1 câu):
- Các sub-theme (2–3 gạch đầu dòng):
- Message (1–2 câu: câu chuyện muốn nói điều gì về con người / cuộc sống?):

5. MAIN CHARACTERS (NHÂN VẬT CHÍNH)
Cho từng nhân vật quan trọng:
- Name:
- Role: (Protagonist / Deuteragonist / Antagonist / Mentor / Comic relief / ...)
- Short description (2–3 câu):
- Goal (họ muốn gì?):
- Inner Need (họ thiếu gì trong nội tâm?):
- Flaw / Weakness (yếu điểm?):
- Change Arc (dự kiến thay đổi thế nào từ đầu → cuối mùa?):
- Key relationships (xung đột / gắn kết với ai?):

6. MAIN ANTAGONIST / FORCE OF CONFLICT (PHẢN DIỆN / THẾ LỰC ĐỐI KHÁNG)
- Là ai / là thế lực gì?
- Mục tiêu / động cơ:
- Phương thức gây xung đột:
- Tại sao khó đánh bại?

7. SEASON ARC (CUNG TRUYỆN CẢ MÙA)
- Opening situation (trạng thái ban đầu):
- Mid-season turning point (bước ngoặt giữa mùa):
- Pre-finale crisis (khủng hoảng trước cuối mùa):
- Season climax (điểm đỉnh cao của cả mùa):
- Season resolution (mức độ giải quyết, còn treo lại điều gì?):

8. CORE MISSION (NHIỆM VỤ XUYÊN SUỐT)
- Một câu tóm tắt: “Mùa phim này thực chất là hành trình ...”
- Nếu có vật thể / mục tiêu cụ thể (vd: 7 mảnh phong ấn, 5 cánh cổng, ...), hãy liệt kê.

9. SERIES ENGINE / MOTIF (MÔ TÍP VẬN HÀNH SERIES)
- Kiểu series: (Quest / Monster of the Week / Mystery / Character-driven / Political / ...)
- Mỗi tập xoay quanh loại nhiệm vụ / đối thủ / tình huống gì?
- Mẫu kết quả thường thấy: (thắng nhỏ, thua tạm thời, trade-off,...)

10. EPISODE TEMPLATE (MẪU 1 TẬP – RÀNG BUỘC 3 QUY TẮC VÀNG)
Mỗi tập phải tuân theo:

- MISSION:
  • Mỗi tập PHẢI có 1 nhiệm vụ rõ ràng.

- COLD OPEN:
  • Cảnh mở đầu gây sốc, hook mạnh.

- ACT 1 – SETUP:
  • Thiết lập nhiệm vụ & điều kiện xuất phát.

- ACT 2 – CONFLICT + TWIST:
  • Xung đột tăng dần.
  • BẮT BUỘC có một TWIST ý nghĩa (phản bội, bẫy, thông tin mới, đảo chiều...).

- ACT 3 – CLIMAX:
  • Khoảnh khắc đỉnh nhất của tập (chiến đấu, lựa chọn, hy sinh, revelation...).

- ACT 4 – RESOLUTION:
  • Hậu quả & dư âm cảm xúc.

- CLIFFHANGER:
  • Câu hỏi hoặc hình ảnh treo dẫn sang tập sau.

11. EPISODE COUNT & LENGTH (SỐ TẬP & ĐỘ DÀI)
- Số tập dự kiến:
- Thời lượng ước tính mỗi tập (nếu có):
- Số scene ước tính / tập (vd: 8–12):

12. CENTRAL QUESTIONS (CÁC CÂU HỎI TRUNG TÂM)
- 3–5 câu hỏi lõi mà nếu trả lời hết → hoàn thành mùa phim.

13. TONE & PACING (NHỊP VÀ KHÔNG KHÍ)
- Pacing: (nhanh / vừa / chậm, nhiều hành động hay nhiều thoại?)
- Humor level: (ít / vừa / nhiều)
- Darkness level: (nhẹ / trung bình / u tối)

14. NOTES FOR CHAPTER GENERATION (GHI CHÚ CHO BƯỚC TẠO CHƯƠNG – B3)
- Những điều BẮT BUỘC phải lặp lại / nhấn mạnh (motif, biểu tượng, câu thoại,...)
- Những rule thế giới KHÔNG ĐƯỢC PHÁ VỠ.
- Những lưu ý về nhân vật, tuyến nhân vật cần được phát triển dần theo tập.

============================================================
YÊU CẦU ĐẦU RA:
- Hãy TRỰC TIẾP điền đầy đủ nội dung vào mẫu STORY LOCK-IN TEMPLATE trên.
- Giữ nguyên tiêu đề các mục (1. 2. 3. ...) và thứ tự.
- Không thêm ghi chú ngoài template.
- Không trả về JSON.
============================================================
"""


def main():
    print("📚 B2 – Tạo STORY LOCK-IN từ story_idea.txt")
    print("-------------------------------------------------")

    if not STORY_IDEA_FILE.exists():
        print(f"❌ Không tìm thấy file {STORY_IDEA_FILE.name}.")
        print("➡ Hãy chắc chắn bạn đã có B1 (story_idea.txt) trước khi chạy B2.")
        sys.exit(1)

    story_idea_text = STORY_IDEA_FILE.read_text(encoding="utf-8").strip()
    if not story_idea_text:
        print("❌ File story_idea.txt đang trống.")
        print("➡ Hãy nhập / chỉnh sửa nội dung B1 trước.")
        sys.exit(1)

    print(f"📖 Đã đọc STORY IDEA từ {STORY_IDEA_FILE.name} (độ dài {len(story_idea_text)} ký tự).")
    print("🧠 Đang gọi AI để sinh STORY LOCK-IN (B2)...")
    print("   (Bước này có thể mất vài giây tuỳ độ dài nội dung.)")

    user_prompt = USER_PROMPT_TEMPLATE.format(
        story_idea_text=story_idea_text
    )

    try:
        lock_in_text = call_gemini_text(
            prompt=user_prompt,
            system_prompt=SYSTEM_PROMPT,
            max_output_tokens=4096,
        )
    except Exception as e:
        print("❌ Lỗi khi gọi AI để tạo STORY LOCK-IN.")
        print(f"Chi tiết lỗi: {e}")
        sys.exit(1)

    lock_in_text = (lock_in_text or "").strip()
    if not lock_in_text:
        print("❌ AI trả về nội dung rỗng. Không thể tạo story_lock_in.txt.")
        sys.exit(1)

    STORY_LOCK_IN_FILE.write_text(lock_in_text, encoding="utf-8")

    print(f"✅ Đã ghi STORY LOCK-IN vào: {STORY_LOCK_IN_FILE.name}")
    print("➡ Bạn có thể mở file này, đọc lại, chỉnh sửa thêm nếu muốn.")
    print("➡ Sau đó chạy B3 (generate_chapters.py) để sinh CHAPTERS theo công thức 6 phần + 3 Quy tắc vàng.")


if __name__ == "__main__":
    main()
