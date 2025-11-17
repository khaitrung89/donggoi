import re
from pathlib import Path

RAW_FILE = "raw_scenes.txt"
OUTPUT_FILE = "scenes.txt"

# Regex nhận diện đầu cảnh:
# Hỗ trợ:
#   Scene 1:
#   SCENE 2 -
#   Scene 3.
#   Cảnh 4:
#   CẢNH 5 -
SCENE_HEADER_PATTERN = re.compile(
    r'^\s*(scene|SCENE|Scene|cảnh|Cảnh|CẢNH)\s+(\d+)\s*[:\-\.]?\s*(.*)$'
)


def parse_raw_scenes(text: str):
    """
    Tách nội dung raw thành list cảnh.
    Mỗi phần tử: (scene_number, scene_text)
    """
    lines = text.splitlines()

    scenes = []
    current_num = None
    current_lines = []

    def flush_scene():
        nonlocal current_num, current_lines, scenes
        if current_num is not None:
            # Ghép nội dung cảnh
            body = "\n".join(current_lines).strip()
            if body:
                scenes.append((current_num, body))
        current_num = None
        current_lines = []

    for line in lines:
        m = SCENE_HEADER_PATTERN.match(line)
        if m:
            # Gặp header cảnh mới
            # 1) lưu cảnh cũ (nếu có)
            flush_scene()

            header_word = m.group(1)  # Scene / Cảnh
            num_str = m.group(2)      # số cảnh
            tail = m.group(3).strip() # phần còn lại sau dấu : - .

            try:
                current_num = int(num_str)
            except ValueError:
                # Nếu có gì kỳ, bỏ qua số, sẽ đánh lại index sau
                current_num = None

            # Khởi tạo nội dung cảnh mới
            current_lines = []
            if tail:
                # Nếu ngay header đã có nội dung, đưa vào body
                current_lines.append(tail)
        else:
            # Không phải header → nội dung cảnh hiện tại
            if current_num is not None:
                current_lines.append(line)
            else:
                # Chưa gặp header nhưng đã có text – thường bỏ qua
                # hoặc bạn có thể gom vào "Scene 1" nếu muốn
                pass

    # Flush cảnh cuối cùng
    flush_scene()

    return scenes


def main():
    raw_path = Path(RAW_FILE)
    if not raw_path.exists():
        print(f"❌ Không tìm thấy file {RAW_FILE}. Hãy tạo file này và dán scenes vào.")
        return

    raw_text = raw_path.read_text(encoding="utf-8")
    if not raw_text.strip():
        print(f"❌ File {RAW_FILE} đang trống.")
        return

    scenes = parse_raw_scenes(raw_text)
    if not scenes:
        print("⚠️ Không tìm được cảnh nào. Kiểm tra định dạng header (Scene 1:, Cảnh 2-, ...).")
        return

    # Ghi ra scenes.txt theo format:
    # Scene 1: ...
    # Scene 2: ...
    out_path = Path(OUTPUT_FILE)
    with out_path.open("w", encoding="utf-8") as f:
        for idx, (num, body) in enumerate(scenes, start=1):
            # Dùng idx làm số cảnh chính thức (1,2,3,...) cho chắc ăn
            line = f"Scene {idx}: {body.strip()}"
            f.write(line + "\n")

    print(f"✅ Đã tách được {len(scenes)} cảnh và lưu vào {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
