import google.generativeai as gen
import json
from pathlib import Path

# ==============================
# FILE CONFIG
# ==============================

API_KEYS_FILE = "api_keys.txt"
SCENES_FILE = "scenes.txt"
OUTPUT_FILE = "output_prompts.txt"
CHARACTER_DICT_FILE = "character_dictionary.json"


# ==============================
# LOAD API KEYS
# ==============================

def load_api_keys(path: str = API_KEYS_FILE):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Không tìm thấy {path}")
    keys = [line.strip() for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
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
# LOAD SCENES
# ==============================

def load_scenes(path: str = SCENES_FILE):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Không tìm thấy {SCENES_FILE}")
    raw_lines = [line.strip() for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    scenes = []
    for line in raw_lines:
        if ":" in line:
            prefix, rest = line.split(":", 1)
            if prefix.lower().startswith("scene"):
                scenes.append(rest.strip())
            else:
                scenes.append(line)
        else:
            scenes.append(line)
    print(f"📚 Đã nạp {len(scenes)} cảnh từ {SCENES_FILE}")
    return scenes


# ==============================
# LOAD CHARACTER DICT
# ==============================

def load_character_dict(path: str = CHARACTER_DICT_FILE):
    p = Path(path)
    if not p.exists():
        print("⚠️ Không tìm thấy character_dictionary.json, sẽ dùng mặc định LANA/ADAI/ASUKA.")
        return {"LANA": {}, "ADAI": {}, "ASUKA": {}}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
        print("⚠️ character_dictionary.json không phải dict, fallback.")
        return {"LANA": {}, "ADAI": {}, "ASUKA": {}}
    except Exception as e:
        print(f"⚠️ Lỗi đọc character_dictionary.json: {e}")
        return {"LANA": {}, "ADAI": {}, "ASUKA": {}}


# ==============================
# PROMPT TEMPLATE (EPIC + POV + CLOSE-UP)
# ==============================

PROMPT_TEMPLATE = r"""
You are a cinematic JSON generator for AI video production.

ALLOWED MAIN CHARACTERS:
{allowed_names}

GLOBAL RULES:
- Do NOT create any new named characters.
- Background characters must stay UNNAMED ("guards", "villagers", "spirits", "beasts", ...).
- Output MUST be valid JSON on a SINGLE LINE.
- All text MUST be in natural ENGLISH.

### EPIC CAMERA PRIORITY ###
- Prioritize shot_types: "wide", "medium".
- Use "close-up" or "extreme close-up" ONLY when:
  * the scene centers on emotional reaction,
  * intense dialogue between main characters,
  * an important decision or revelation,
  * farewell, sacrifice, inner conflict, or a symbolic detail.
- Epic fantasy / mythic environments (mountains, deserts, temples, titans, celestial spaces)
  MUST default to wide cinematic framing unless there is a very strong reason to go close.
- Camera style should feel grand, mythic, sweeping, large-scale.
  Examples:
    "epic wide aerial establishing over the ancient city",
    "sweeping crane shot around the colossal titan",
    "slow panoramic dolly across the ruined temple plaza".

### EMOTIONAL CLOSE-UP RULE ###
- In a minority of scenes (about 15–30% of all scenes that clearly focus on character emotion),
  you SHOULD choose "close-up" or "extreme close-up" to emphasize the face and subtle expression.
- Those close scenes are usually:
  * confrontations between main characters,
  * moments of doubt, fear, grief, rage, or tenderness,
  * when a single action (tears, trembling hand, blood drop, symbol) is extremely important.

### POV RULE (YOU MUST DIVERSIFY) ###
"pov" must be one of:
- "third_person"   → default epic cinematic framing
- "over_shoulder"  → conversations, confrontations between two characters
- "first_person"   → when we should feel what one character feels (visions, disorientation, inner fear)
- "god_view"       → large-scale battles, rituals, massive spaces, strategic overview

Guidelines:
- Most scenes can stay "third_person".
- Use "over_shoulder" especially in dialogue-heavy scenes between main characters.
- Use "god_view" for big arenas, large crowds, titan-scale moments, battles, or world-level events.
- Use "first_person" occasionally for scenes where a character is overwhelmed, experiencing visions,
  illusions, or stepping into a dangerous unknown where we should share their perception.

### CLOSE-UP NAME RULE ###
If "shot_type" is "close-up" or "extreme close-up":
- In "focus_characters", for any main character you MUST use the "Name2" variant.
  Example:
    LANA  → LANA2
    ADAI  → ADAI2
    ASUKA → ASUKA2
If "shot_type" is "wide" or "medium":
- In "focus_characters", use the normal names without suffix (LANA, ADAI, ASUKA).
The "character.name" field should ALWAYS use the normal name (without "2"),
or "NONE" if there is no single clear focus character.

### JSON FORMAT (STRICT) ###
Produce EXACTLY ONE JSON object with this structure:

{{
  "scene_number": {scene_number},
  "scene_title": "...",
  "scene_summary": "...",
  "character": {{
    "name": "[main focus name or \"NONE\"]",
    "emotions": {{"primary": "...", "secondary": "..."}},
    "voice_tone": "..."
  }},
  "cinematic": {{
    "camera": "...",
    "shot_type": "[wide | medium | close-up | extreme close-up]",
    "pov": "[third_person | over_shoulder | first_person | god_view]",
    "focus_characters": ["Name1", "Name2"],
    "lighting": "...",
    "environment": "...",
    "movement": "..."
  }},
  "dialogue": {{
    "characters": [
      {{"speaker": "Name1", "line": "Dialogue line 1..."}},
      {{"speaker": "Name2", "line": "Dialogue line 2..."}}
    ]
  }},
  "action_block": {{
    "length": "120-180 words",
    "content": "Natural English cinematic description of the scene, 120-180 words."
  }}
}}

ADDITIONAL DIALOGUE RULES:
- Speakers must ONLY be from the allowed main character names.
- If the scene has no dialogue, set "characters": [].

ACTION BLOCK RULES:
- 120-180 words.
- Focus on what the camera sees and hears: motion, space, light, danger, emotion.
- Avoid long inner monologue; show emotions via actions, body language, environment.

SCENE DESCRIPTION (may be any language, you MUST think and write in English):
\"\"\"{scene_text}\"\"\"
"""


# ==============================
# CALL GEMINI
# ==============================

def call_gemini(prompt: str) -> str:
    global current_key_index
    for _ in range(len(API_KEYS)):
        try:
            model = gen.GenerativeModel("models/gemini-2.5-flash")
            resp = model.generate_content(prompt)
            text = (resp.text or "").strip()
            if text.startswith("```"):
                text = text.replace("```", "").strip()
            return " ".join(text.split())
        except Exception as e:
            print(f"⚠️ Lỗi với key #{current_key_index + 1}: {e}")
            print("🔄 Đang đổi sang API key tiếp theo...")
            switch_key()
    raise Exception("❌ Tất cả API key đều lỗi hoặc hết quota trong call_gemini().")


# ==============================
# MAIN
# ==============================

def main():
    scenes = load_scenes()
    char_dict = load_character_dict()
    allowed_names = ", ".join(char_dict.keys())
    print(f"👥 Allowed character names: {allowed_names}")

    out_path = Path(OUTPUT_FILE)
    with out_path.open("w", encoding="utf-8") as f:
        for idx, scene in enumerate(scenes, start=1):
            print(f"⏳ Đang xử lý cảnh {idx}/{len(scenes)}...")
            full_prompt = PROMPT_TEMPLATE.format(
                allowed_names=allowed_names,
                scene_number=idx,
                scene_text=scene
            )
            json_line = call_gemini(full_prompt)
            f.write(json_line + "\n")

    print(f"\n✅ Xong! Đã lưu {len(scenes)} prompt vào {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
