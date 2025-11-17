import json
from pathlib import Path

# ==========================
# CẤU HÌNH TÊN FILE
# ==========================

INPUT_FILE = "output_prompts.txt"          # file gốc do generate_prompts.py tạo ra
OUTPUT_FILE = "output_prompts_fixed.txt"   # file sau khi sửa focus_characters


# ==========================
# HÀM HỖ TRỢ
# ==========================

def is_closeup_shot(shot_type: str) -> bool:
    """
    Xác định shot_type có phải close-up / extreme close-up không.
    Chấp hết kiểu: 'close-up', 'Close up', 'CLOSEUP', 'extreme close up', ...
    """
    if not isinstance(shot_type, str):
        return False
    s = shot_type.strip().lower()
    base = s.replace(" ", "").replace("-", "")
    return base in ("closeup", "extremecloseup")


def fix_focus_characters_for_closeup(data: dict) -> dict:
    """
    - Nếu shot_type là close-up / extreme close-up:
      -> Đổi tên trong focus_characters sang name_closeup nếu có
         dựa trên fixed_character_definitions.
    - Nếu không phải close-up thì giữ nguyên.
    """
    cinematic = data.get("cinematic", {})
    shot_type = cinematic.get("shot_type")

    if not is_closeup_shot(shot_type):
        # Không phải close-up / extreme close-up -> giữ nguyên
        return data

    focus = cinematic.get("focus_characters")
    if not isinstance(focus, list):
        return data

    fixed_defs = data.get("fixed_character_definitions", {})

    new_focus = []
    for name in focus:
        # Nếu name có trong fixed_character_definitions và có name_closeup -> dùng name_closeup
        if isinstance(name, str) and name in fixed_defs:
            close_name = fixed_defs[name].get("name_closeup")
            if isinstance(close_name, str) and close_name.strip():
                new_focus.append(close_name.strip())
            else:
                # fallback: nếu không có name_closeup, tự thêm '2'
                new_focus.append(name + "2")
        else:
            # Không có trong dictionary -> giữ nguyên
            new_focus.append(name)

    cinematic["focus_characters"] = new_focus
    data["cinematic"] = cinematic
    return data


# ==========================
# MAIN
# ==========================

def main():
    in_path = Path(INPUT_FILE)
    if not in_path.exists():
        print(f"❌ Không tìm thấy file input: {INPUT_FILE}")
        return

    lines = in_path.read_text(encoding="utf-8").splitlines()
    if not lines:
        print(f"⚠️ File {INPUT_FILE} trống.")
        return

    out_path = Path(OUTPUT_FILE)
    out_f = out_path.open("w", encoding="utf-8")

    fixed_count = 0
    total = 0

    for idx, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue

        total += 1

        try:
            data = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"⚠️ Dòng {idx}: JSON lỗi, ghi nguyên văn. Lỗi: {e}")
            out_f.write(line + "\n")
            continue

        before_focus = data.get("cinematic", {}).get("focus_characters")

        data = fix_focus_characters_for_closeup(data)

        after_focus = data.get("cinematic", {}).get("focus_characters")

        # Nếu có sự thay đổi focus_characters -> tăng counter
        if before_focus != after_focus:
            fixed_count += 1

        out_line = json.dumps(data, ensure_ascii=False)
        out_f.write(out_line + "\n")

    out_f.close()

    print(f"✅ Hoàn thành! Đã xử lý {total} dòng.")
    print(f"✨ Số cảnh close-up được đổi focus_characters sang name_closeup: {fixed_count}")
    print(f"📄 File output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
