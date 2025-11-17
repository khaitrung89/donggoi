# generate_scenes_from_chapters.py (FINAL v3.0)

import google.generativeai as gen
from pathlib import Path

API_KEYS_FILE = "api_keys.txt"
CHAPTERS_FILE = "chapters.txt"
SCENES_FILE = "scenes.txt"


# ==========================
# CHỌN SỐ CẢNH TỔNG
# ==========================

def choose_scene_mode():
    """
    Hiển thị các gợi ý về mật độ cảnh cho người dùng,
    nhưng cho phép nhập TỰ DO số cảnh mong muốn.
    """
    print("🎬 Chọn mức độ phân cảnh (scene density suggestion):")
    print("  1) Compact  (~40 scenes)   → khoảng 3–4 cảnh / chapter")
    print("  2) Standard (~70 scenes)   → khoảng 5–6 cảnh / chapter")
    print("  3) Epic     (~100+ scenes) → khoảng 8–9 cảnh / chapter")
    print("  4) Custom   (bạn có thể nhập BẤT KỲ số cảnh nào)")

    scenes_input = input("👉 Số phân cảnh bạn muốn (vd: 36, 60, 72, 100...): ").strip()

    # Cố gắng parse số cảnh
    try:
        total_scenes = int(scenes_input)
        if total_scenes < 1:
            raise ValueError()
    except Exception:
        print("⚠️ Số cảnh không hợp lệ. Dùng mặc định: 70 scenes.")
        total_scenes = 70

    # Chia đều cho 12 chương (lấy floor)
    scenes_per_chapter = max(1, total_scenes // 12)

    # Chọn mức độ chi tiết mô tả dựa trên tổng số cảnh
    if total_scenes <= 45:
        detail_level = "concise but still cinematic"
    elif total_scenes <= 85:
        detail_level = "rich cinematic detail and clear beats"
    else:
        detail_level = "very detailed, multi-step cinematic sequences"

    print(f"✅ Chọn: {total_scenes} cảnh tổng → {scenes_per_chapter} cảnh/chapter.")
    print(f"   → Detail level: {detail_level}")

    return {
        "label": f"Custom ({total_scenes} scenes)",
        "min_scenes_per_chapter": scenes_per_chapter,
        "max_scenes_per_chapter": scenes_per_chapter,
        "detail_level": detail_level,
    }


# ==========================
# LOAD API KEY
# ==========================

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


# ==========================
# PROMPT TEMPLATE
# ==========================

SCENE_SPLIT_PROMPT_TEMPLATE = """
You are a professional cinematic scene planner.

INPUT:
The user provides a story outline divided into CHAPTERS.

YOUR TASK:
Break the entire outline into a list of CINEMATIC SCENES with:
- clear visual setting (where it happens, environment)
- clear action or emotional beat
- strong cinematic detail: environment, mood, motion, danger, sound

SCENE COUNT RULE:
For each chapter, generate between {min_scenes} and {max_scenes} scenes.
Detail level: {detail_level}.
Each scene description should make it easy to later design camera angles,
lighting, and character actions.

CHARACTER RULES:
- ONLY use named characters in the outline (for example: LANA, ADAI, ASUKA).
- NO new named characters allowed (do NOT invent names like "Kael", "Ava", etc.).
- You may use generic secondary characters (guards, spirits, beasts, villagers, soldiers…),
  but they must remain unnamed and generic.

STRICT OUTPUT FORMAT:
You MUST output a single flat list of scenes, numbered globally, like this:

Scene 1: [Short English description of the scene...]
Scene 2: [Short English description of the scene...]
Scene 3: [Short English description of the scene...]
...

- Do NOT reset numbering per chapter.
- Do NOT include chapter headers in the output.
- Do NOT write explanations before or after the list.
- All text must be in NATURAL ENGLISH.

TONE:
- Mythic, cinematic, and visually oriented.
- Focus on what can be SEEN and HEARD (actions, environments, conflicts),
  not long internal monologues.

CHAPTER OUTLINE:
\"\"\"{chapters_text}\"\"\"
"""


# ==========================
# CALL GEMINI
# ==========================

def call_gemini(prompt: str) -> str:
    """
    Gọi Gemini sinh danh sách SCENES, tự xoay vòng API key nếu lỗi.
    """
    global current_key_index

    for _ in range(len(API_KEYS)):
        try:
            model = gen.GenerativeModel("models/gemini-2.5-flash")
            resp = model.generate_content(prompt)
            text = (resp.text or "").strip()

            # Nếu model trả về trong ``` ``` thì bỏ đi
            if text.startswith("```"):
                text = text.replace("```", "").strip()

            return text

        except Exception as e:
            print(f"⚠️ Lỗi với key #{current_key_index + 1}: {e}")
            print("🔄 Đổi key…")
            switch_key()

    raise Exception("❌ Tất cả API key đều lỗi hoặc hết quota khi sinh SCENES.")


# ==========================
# MAIN
# ==========================

def main():
    # 1) User chọn số cảnh mong muốn (tự do)
    mode_cfg = choose_scene_mode()
    min_scenes = mode_cfg["min_scenes_per_chapter"]
    max_scenes = mode_cfg["max_scenes_per_chapter"]
    detail_level = mode_cfg["detail_level"]

    # 2) Đọc chapters.txt
    chapters_path = Path(CHAPTERS_FILE)
    if not chapters_path.exists():
        print(f"❌ Không tìm thấy {CHAPTERS_FILE}. Hãy chạy generate_chapters_from_idea.py trước.")
        return

    chapters_text = chapters_path.read_text(encoding="utf-8").strip()
    if not chapters_text:
        print(f"❌ File {CHAPTERS_FILE} đang trống.")
        return

    # 3) Build prompt
    prompt = SCENE_SPLIT_PROMPT_TEMPLATE.format(
        min_scenes=min_scenes,
        max_scenes=max_scenes,
        detail_level=detail_level,
        chapters_text=chapters_text,
    )

    print("⏳ Đang sinh danh sách SCENES từ CHAPTERS...")
    scenes_text = call_gemini(prompt)

    # 4) Ghi scenes.txt
    out_path = Path(SCENES_FILE)
    out_path.write_text(scenes_text.strip(), encoding="utf-8")

    print(f"✅ Đã tạo xong SCENES và lưu vào {SCENES_FILE}")
    print("ℹ️ Hãy mở scenes.txt để xem tổng số cảnh và nội dung trước khi chạy generate_prompts.py.")


if __name__ == "__main__":
    main()
