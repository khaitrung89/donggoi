import google.generativeai as gen
import json
import random
from pathlib import Path

from layer_rules import CORE_RULES
from layer_filters import apply_closeup_name_switch, enforce_allowed_characters

# ==============================
# KIỂM TRA LICENSE BẢN QUYỀN
# ==============================
try:
    from license_manager import check_license, request_license
    
    # Kiểm tra license trước khi chạy tool
    if not check_license():
        print("⚠️ Tool chưa được kích hoạt bản quyền!")
        if not request_license():
            print("❌ Không thể kích hoạt bản quyền. Tool sẽ thoát.")
            exit(1)
        else:
            print("✅ Đã kích hoạt bản quyền thành công!")
    else:
        print("✅ License hợp lệ - Tool đã được kích hoạt.")
        
except ImportError:
    print("⚠️ Không tìm thấy module license_manager.py")
    print("⚠️ Tool sẽ chạy ở chế độ demo (không có bản quyền)")
    print("⚠️ Để kích hoạt bản quyền, vui lòng chạy: python license_manager.py")

# ==============================
# CẤU HÌNH
# ==============================

API_KEYS_FILE = "api_keys.txt"
SCENES_FILE = "scenes.txt"
OUTPUT_FILE = "output_prompts.txt"
CHARACTER_DICT_FILE = "character_dictionary.json"
CAMERA_STYLES_FILE = "camera_styles.txt"
EXTRAS_WORLDS_FILE = "extras_worlds.json"

# Chọn world cho kịch bản này: "modern" / "medieval" / "fantasy"
WORLD_TYPE = "medieval"


# ==============================
# 1. LOAD API KEYS
# ==============================

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


# ==============================
# 2. LOAD SCENES
# ==============================

def load_scenes(path: str = SCENES_FILE):
    """
    Đọc file scenes.txt và tách thành từng cảnh dạng:
        Scene 1: ...
        Scene 2: ...
    Trả về list string, mỗi phần tử là toàn bộ nội dung "Scene X: ...."
    """
    p = Path(path)
    if not p.exists():
        print(f"⚠️ Không tìm thấy {path}")
        return []

    text = p.read_text(encoding="utf-8").strip()
    if not text:
        return []

    blocks = []
    parts = text.split("Scene ")
    for part in parts[1:]:
        if ":" not in part:
            continue
        num, rest = part.split(":", 1)
        num = num.strip()
        content = rest.strip()
        if not content:
            continue
        blocks.append(f"Scene {num}: {content}")
    return blocks


scenes = load_scenes()
print(f"📚 Đã nạp {len(scenes)} cảnh từ {SCENES_FILE}")


# ==============================
# 3. LOAD CHARACTER DICTIONARY (chỉ dùng name_closeup)
# ==============================

def load_character_dictionary(path: str = CHARACTER_DICT_FILE):
    """
    Bản SUPER LITE: chỉ dùng để lấy name_closeup cho Alex/Maya/Marcus
    """
    p = Path(path)
    if not p.exists():
        print(
            f"⚠️ Không tìm thấy {path}, vẫn chạy được nhưng close-up sẽ dùng name+'2'."
        )
        return {}

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"⚠️ Lỗi đọc/parse {path}: {e}")
        return {}

    characters = {}
    for char in data.get("characters", []):
        name = char.get("name")
        if not name:
            continue
        characters[name] = {
            "name": name,
            "name_closeup": char.get("name_closeup", name + "2"),
        }

    print(f"👥 Đã nạp {len(characters)} nhân vật từ {CHARACTER_DICT_FILE}")
    return characters


character_dict = load_character_dictionary()


# ==============================
# 4. LOAD CAMERA STYLES
# ==============================

def load_camera_styles(path: str = CAMERA_STYLES_FILE):
    """
    Đọc danh sách camera từ file .txt, bỏ dòng trống và dòng bắt đầu bằng '#'.
    """
    p = Path(path)
    if not p.exists():
        print(f"⚠️ Không tìm thấy {path}, AI sẽ tự chọn camera.")
        return []

    lines = p.read_text(encoding="utf-8").splitlines()
    cameras = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cameras.append(line)

    print(f"🎥 Đã nạp {len(cameras)} kiểu camera từ {CAMERA_STYLES_FILE}")
    return cameras


camera_styles = load_camera_styles()
last_camera = None
last_shot_type = None


# ==============================
# 5. LOAD EXTRAS WORLDS
# ==============================

def load_extras_worlds(path: str = EXTRAS_WORLDS_FILE):
    p = Path(path)
    if not p.exists():
        print(
            f"⚠️ Không tìm thấy {path}, sẽ không cung cấp gợi ý nhân vật phụ theo world."
        )
        return {}

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"⚠️ Lỗi đọc/parse {path}: {e}")
        return {}
    return data


extras_worlds = load_extras_worlds()


def build_extras_world_description(world_type: str) -> str:
    """
    Tạo đoạn mô tả ngắn về các loại nhân vật phụ có sẵn cho world hiện tại
    để nhét vào prompt cho model lựa.
    """
    world = extras_worlds.get(world_type, {})
    roles = world.get("roles", [])
    if not roles:
        return (
            "No predefined secondary character roles. "
            "You should keep backgrounds minimal and generic."
        )

    lines = []
    lines.append(f"CURRENT WORLD TYPE: {world_type.upper()}")
    lines.append("You may use these types of unnamed secondary characters:")
    for r in roles:
        id_prefix = r.get("id_prefix", "")
        role = r.get("role", "")
        appearance = r.get("appearance", "")
        lines.append(f"- ROLE KEY '{id_prefix}': {role} — {appearance}")
    lines.append(
        "You must keep them unnamed and only describe them by role and appearance."
    )
    return "\n".join(lines)


extras_world_desc = build_extras_world_description(WORLD_TYPE)


# ==============================
# 6. PROMPT TEMPLATE (SUPER LITE - KHÔNG appearance)
# ==============================

PROMPT_TEMPLATE = """
You are a cinematic formatter.

IMPORTANT LANGUAGE RULE:
- ALL TEXT VALUES in the JSON MUST be in NATURAL ENGLISH only.
- The input scene description may contain Vietnamese or mixed language,
  but you MUST rewrite EVERYTHING in ENGLISH in the output JSON.
- This includes: scene_title, setting, cinematic fields, dialogue lines,
  action_block, emotions, voice_tone descriptions, etc.

<<CORE_RULES>>

SECONDARY CHARACTERS WORLD CONTEXT:
<<EXTRAS_WORLD_DESC>>

CAMERA STYLE OPTIONS (use EXACTLY one of these values for the "camera" field):
<<CAMERA_LIST>>

Convert the following ENGLISH scene into ONE SINGLE LINE JSON, EXACTLY in this structure:

{"scene_number":1,
 "scene_title":"[Short title]",
 "character":{
    "name":"[Main character name]",
    "emotions":{
        "primary":"[Primary emotion]",
        "secondary":"[Secondary emotion]"
    },
    "voice_tone":"[Voice tone that matches the scene]"
 },
 "setting":{
   "location":"[Place]",
   "environment":"[Environment]",
   "time":"[Day/Night]"
 },
 "cinematic":{
   "camera":"[One camera style from CAMERA STYLE OPTIONS above]",
   "shot_type":"[wide/medium/close-up/extreme close-up]",
   "focus_characters":["[character names in this shot]"],
   "lighting":"[Lighting - auto-select]",
   "mood":"[Mood]",
   "style":"Cinematic 8K realistic",
   "effects":"[Effects - auto-select]",
   "sound":"[Ambience]"
 },
 "dialogue":{
   "characters":[
     {"speaker":"[Speaker name]","line":"[Dialogue line]"}
   ]
 },
 "action_block":{
   "length":"150-200 words",
   "content":"[Cinematic action description]"
 }
}

IMPORTANT CHARACTER DESCRIPTION RULE:
- In the "character" block, you MUST NOT output the field "appearance".
- Only include: name, emotions, voice_tone.
- If you want to show how the character looks, moves, or reacts,
  describe it inside the free text of "action_block.content" instead,
  not as a static profile field.

CRITICAL CAMERA & CLOSE-UP RULES (RECAP):
- If shot_type is "close-up" or "extreme close-up", focus_characters must be
  Alex2, Maya2, Marcus2 (or some combination among them).
- If shot_type is "medium" or "wide", focus_characters must be
  Alex, Maya, Marcus (or some combination among them).
- Secondary characters must NEVER appear as focus_characters or dialogue speakers.
- Secondary characters can appear only in the free text description (action_block).

OUTPUT FORMAT:
- Return ONLY valid JSON.
- JSON MUST be ONE SINGLE LINE (no line breaks).
- action_block.content MUST be around 150-200 words.

ENGLISH SCENE TO PROCESS:
\"\"\"<<SCENE>>\"\"\"
"""


# ==============================
# 7. PROMPT DỊCH SCENE → ENGLISH
# ==============================

SCENE_TRANSLATE_PROMPT = """
You are a professional translator for cinematic scripts.

TASK:
Translate the following scene description into NATURAL, FLUENT ENGLISH.
The input may be in Vietnamese or mixed language, but you MUST output ONLY ENGLISH.

RULES:
1. Keep all character names (Alex, Maya, Marcus, etc.) unchanged.
2. Do NOT add new story details, only translate and lightly smooth the text.
3. Do NOT output any JSON.
4. Return ONLY the translated scene text, as plain English, one or a few paragraphs.

SCENE:
<<SCENE>>
"""


# ==============================
# 8. GỌI GEMINI
# ==============================

def call_gemini(prompt: str) -> str:
    """
    Gọi Gemini sinh JSON 1 dòng. Tự xoay vòng API keys nếu lỗi.
    """
    global current_key_index

    for _ in range(len(API_KEYS)):
        try:
            model = gen.GenerativeModel("models/gemini-2.5-flash")
            resp = model.generate_content(prompt)
            text = (resp.text or "").strip()

            # Clean nếu model trả dưới dạng ```json ... ```
            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            one_line = " ".join(text.splitlines()).strip()
            return one_line

        except Exception as e:
            print(f"⚠️ Lỗi với key #{current_key_index + 1}: {e}")
            print("🔄 Đổi sang API key tiếp theo...")
            switch_key()

    raise Exception("❌ Tất cả API key đều lỗi hoặc hết quota.")


def translate_scene_to_english(scene_text: str) -> str:
    """
    Dịch 1 scene (có thể tiếng Việt) sang tiếng Anh thuần
    để đưa vào PROMPT_TEMPLATE.
    """
    global current_key_index

    prompt = SCENE_TRANSLATE_PROMPT.replace("<<SCENE>>", scene_text)

    for _ in range(len(API_KEYS)):
        try:
            model = gen.GenerativeModel("models/gemini-2.5-flash")
            resp = model.generate_content(prompt)
            text = (resp.text or "").strip()

            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            one_line = " ".join(text.splitlines()).strip()
            return one_line

        except Exception as e:
            print(f"⚠️ Lỗi dịch scene với key #{current_key_index + 1}: {e}")
            print("🔄 Đổi sang API key tiếp theo...")
            switch_key()

    raise Exception("❌ Tất cả API key đều lỗi khi dịch scene sang tiếng Anh.")


# ==============================
# 9. HẬU XỬ LÝ: CAMERA, SHOT_TYPE, CAST, SCENE_NUMBER
# ==============================

def postprocess_camera_and_shottype(data: dict) -> dict:
    """
    - Đảm bảo camera nằm trong danh sách camera_styles.
    - Không cho 2 cảnh liên tiếp dùng cùng camera nếu có thể.
    - Chuẩn hoá shot_type về: wide / medium / close-up / extreme close-up.
    """
    global last_camera, last_shot_type, camera_styles

    cinematic = data.get("cinematic", {}) or {}

    # ----- CAMERA -----
    cam = cinematic.get("camera")
    if isinstance(cam, str):
        cam_stripped = cam.strip()
        if camera_styles:
            # Nếu AI bịa camera không có trong file, random 1 cái hợp lệ
            if cam_stripped not in camera_styles:
                cam_stripped = random.choice(camera_styles)
                cinematic["camera"] = cam_stripped

            # Nếu giống cảnh trước, chọn camera khác
            if last_camera is not None and cam_stripped == last_camera:
                alternatives = [c for c in camera_styles if c != last_camera]
                if alternatives:
                    new_cam = random.choice(alternatives)
                    cinematic["camera"] = new_cam
                    cam_stripped = new_cam

        last_camera = cam_stripped

    # ----- SHOT TYPE -----
    shot = cinematic.get("shot_type")
    if isinstance(shot, str):
        s = shot.strip().lower()
        base = s.replace("-", "").replace(" ", "")

        # Chuẩn hoá
        if "extreme" in base and "close" in base:
            base = "extremecloseup"
            cinematic["shot_type"] = "extreme close-up"
        elif "close" in base:
            base = "closeup"
            cinematic["shot_type"] = "close-up"
        elif "wide" in base:
            base = "wide"
            cinematic["shot_type"] = "wide"
        elif "medium" in base:
            base = "medium"
            cinematic["shot_type"] = "medium"

        # Nếu trùng shot_type trước đó → đổi để đa dạng hơn
        if last_shot_type is not None and base == last_shot_type:
            if base == "medium":
                cinematic["shot_type"] = "close-up"
                base = "closeup"
            elif base in ("closeup", "extremecloseup"):
                cinematic["shot_type"] = "medium"
                base = "medium"
            elif base == "wide":
                cinematic["shot_type"] = "medium"
                base = "medium"

        last_shot_type = base

    data["cinematic"] = cinematic
    return data


def postprocess_json_line(json_line: str, scene_index: int) -> str:
    """
    Parse JSON string, áp dụng:
      - Chuẩn hoá camera & shot_type
      - close-up logic (Alex2/Maya2/Marcus2)
      - lọc nhân vật lạ (chỉ cho Alex/Maya/Marcus + phiên bản 2)
      - GÁN LẠI scene_number = scene_index (1,2,3,... theo thứ tự scenes.txt)

    Trả về: JSON string 1 dòng (SUPER LITE).
    """
    try:
        data = json.loads(json_line)
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON không parse được, ghi raw. Lỗi: {e}")
        return json_line

    # 1) Camera & shot_type
    data = postprocess_camera_and_shottype(data)

    # 2) Close-up name switch: Alex -> Alex2...
    data = apply_closeup_name_switch(data, character_dict)

    # 3) Lọc cast: chỉ cho Alex/Maya/Marcus (+ bản 2) ở focus & speaker
    data = enforce_allowed_characters(data)

    # 4) Gán lại scene_number theo index (bất kể model trả gì)
    data["scene_number"] = int(scene_index)

    return json.dumps(data, ensure_ascii=False)


# ==============================
# 10. MAIN
# ==============================

def main():
    if not scenes:
        print("⚠️ Không có cảnh nào trong scenes.txt – kiểm tra lại file input.")
        return

    # Chuẩn bị CAMERA_LIST string cho prompt
    if camera_styles:
        camera_list_str = "\n".join([f"- {c}" for c in camera_styles])
    else:
        camera_list_str = (
            "- tracking shot\n- medium shot\n- wide shot\n- close-up shot"
        )

    base_template = PROMPT_TEMPLATE.replace("<<CORE_RULES>>", CORE_RULES)
    base_template = base_template.replace("<<EXTRAS_WORLD_DESC>>", extras_world_desc)

    out_path = Path(OUTPUT_FILE)
    with out_path.open("w", encoding="utf-8") as out_f:
        for idx, scene in enumerate(scenes, start=1):
            print(f"⏳ Đang xử lý cảnh {idx}/{len(scenes)}...")

            # 1) Dịch scene (có thể tiếng Việt) sang tiếng Anh
            english_scene = translate_scene_to_english(scene)
            print(f"   → Scene EN (preview): {english_scene[:80]}...")

            # 2) Build prompt JSON formatter
            prompt = base_template.replace("<<CAMERA_LIST>>", camera_list_str)
            prompt = prompt.replace("<<SCENE>>", english_scene)

            # 3) Gọi Gemini sinh JSON 1 dòng
            raw_line = call_gemini(prompt)

            # 4) Hậu xử lý JSON + gán scene_number = idx
            final_line = postprocess_json_line(raw_line, idx)

            # 5) Ghi ra file
            out_f.write(final_line + "\n")

    print(f"\n✅ Xong! Đã lưu {len(scenes)} prompt vào {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
