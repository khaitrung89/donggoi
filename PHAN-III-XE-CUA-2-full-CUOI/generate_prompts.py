import json
import sys
import io
from pathlib import Path
from typing import Any, Dict, List, Tuple

from ai_utils import call_gemini_text, NoValidAPIKeyError

# Fix Unicode encoding on Windows console
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCENES_FILE = Path("scenes.txt")
OUTPUT_FILE = Path("output_prompts.txt")


def load_scenes() -> List[str]:
    """
    Đọc scenes.txt, trả về list dòng (bỏ dòng trống).
    Mỗi dòng có thể là:
      - JSON (ưu tiên)
      - Hoặc plain text mô tả cảnh.
    """
    if not SCENES_FILE.exists():
        raise FileNotFoundError(
            "Không tìm thấy scenes.txt. Hãy chạy generate_scenes_from_chapters.py (B3) trước."
        )

    lines = [
        ln.strip()
        for ln in SCENES_FILE.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    if not lines:
        raise ValueError("scenes.txt đang trống.")
    return lines


def try_parse_scene_line(line: str) -> Tuple[Dict[str, Any] | None, str]:
    """
    Thử parse 1 dòng scenes.txt thành JSON.
    Nếu parse được → (obj, "json")
    Nếu không      → (None, "text")
    """
    try:
        obj = json.loads(line)
        if isinstance(obj, dict):
            return obj, "json"
    except json.JSONDecodeError:
        pass
    return None, "text"


def build_prompt_for_scene(scene_obj: Dict[str, Any] | None, raw_text: str) -> str:
    """
    Tạo prompt tiếng Anh cho Gemini từ 1 scene.
    Nếu scene_obj != None → đã có JSON (scene_number, chapter_number, ...)
    Nếu scene_obj == None → chỉ có mô tả text (raw_text).
    """

    # Chuẩn hoá phần mô tả scene đầu vào cho prompt
    if scene_obj is not None:
        scene_json_pretty = json.dumps(scene_obj, ensure_ascii=False, indent=2)
        scene_info_block = f"""The scene description is given as JSON:

{scene_json_pretty}
"""
    else:
        scene_info_block = f"""The scene description is given as plain text:

\"\"\"{raw_text}\"\"\"
"""

    prompt = f"""
You are a professional cinematic prompt designer for text-to-video models
like Sora, VEO, or Dreamina. Your job is to convert a scene description
into a rich, structured JSON prompt in ENGLISH ONLY.

{scene_info_block}

Your tasks:

1) Understand the narrative context, characters, setting, and emotional beats.
2) Design a cinematic shot with clear camera language and composition.
3) Specify the main character focus, emotions, and voice tone.
4) Provide a short dialogue suggestion (if appropriate) and an action block.

OUTPUT REQUIREMENTS (VERY IMPORTANT):

- You MUST return ONLY ONE JSON object (no extra text).
- All fields and values MUST be in ENGLISH ONLY.
- Use the following JSON structure (you may extend with extra fields if needed,
  but keep these core keys):

{{
  "scene_number": <int or null if unknown>,
  "scene_title": "Short English title",
  "chapter_number": <int or null>,
  "chapter_title": "English chapter title or empty string",

  "character": {{
    "name": "Main character name in ALL CAPS, e.g. LANA / ADAI / ASUKA if applicable",
    "appearance": "One concise sentence describing outfit and look",
    "emotions": {{
      "primary": "Main emotion word (e.g. determined, fearful, calm)",
      "secondary": "Secondary emotion word or empty string"
    }},
    "voice_tone": "English description of how they speak (e.g. tense and breathless)"
  }},

  "setting": {{
    "location": "Concrete location name (rooftop, forest at night, desert canyon...)",
    "time": "Time of day (e.g. dusk, midnight)",
    "weather": "Weather or atmosphere (e.g. rain, heavy fog, clear sky)",
    "description": "2–3 sentences describing environment and mood"
  }},

  "cinematic": {{
    "shot_type": "ONE of: wide, medium, close-up, extreme close-up",
    "pov": "ONE of: third_person, over_shoulder, first_person, profile, tracking",
    "focus_characters": ["List", "of", "character names"],
    "camera_notes": "How camera moves: dolly-in, pan, tilt, handheld, etc.",
    "lighting": "Lighting style (cinematic, harsh backlight, warm firelight, etc.)",
    "environment": "Extra notes: fog, dust, embers, neon lights, etc."
  }},

  "dialogue": {{
    "style": "Short description, e.g. naturalistic, intense, whispering",
    "characters": [
      {{
        "speaker": "NAME IN CAPS or empty string",
        "line": "English dialogue line or empty string"
      }}
    ]
  }},

  "action_block": {{
    "summary": "2–4 sentences describing the physical and emotional action in the shot",
    "beats": [
      "Beat 1 – camera + character action",
      "Beat 2 – important visual or emotional change"
    ]
  }}
}}

Additional rules:
- DO NOT write any Vietnamese.
- DO NOT explain the JSON, DO NOT add commentary.
- DO NOT include backticks or ```json``` markers.
- scene_number / chapter_number: if present in the input JSON, reuse them.

Now generate the JSON object for this scene.
"""
    return prompt


def main():
    print("🎬 B4 – Generate PROMPTS from scenes.txt (EN-only, JSON per line)")

    try:
        lines = load_scenes()
    except Exception as e:
        print(f"❌ Lỗi đọc scenes.txt: {e}")
        return

    out_lines: List[str] = []

    total = len(lines)
    for idx, line in enumerate(lines, start=1):
        print(f"\n🔧 Đang xử lý Scene {idx}/{total}...")

        scene_obj, mode = try_parse_scene_line(line)
        if mode == "json":
            print("📄 Scene input dạng JSON – dùng làm context.")
        else:
            print("📄 Scene input dạng text – dùng mô tả thô.")

        prompt = build_prompt_for_scene(scene_obj, line)

        try:
            json_text = call_gemini_text(prompt)
        except NoValidAPIKeyError as e:
            print(f"❌ Tất cả API key đều lỗi hoặc hết quota: {e}")
            print("⛔ Dừng lại tại scene này.")
            break
        except Exception as e:
            print(f"❌ Lỗi không mong đợi khi gọi Gemini: {e}")
            print("⚠️ Ghi comment lỗi vào output để debug.")
            out_lines.append(f"// ERROR at scene {idx}: {e}")
            continue

        # Đảm bảo kết quả là 1 dòng JSON (nếu Gemini trả nhiều dòng, join lại)
        json_text = json_text.strip()
        if "\n" in json_text:
            # Nếu là JSON pretty, cứ để thế – postprocess sẽ xử lý fallback
            # nhưng để gọn hơn, ta cố gắng parse + dump lại 1 dòng
            try:
                obj = json.loads(json_text)
            except Exception:
                # Không parse được → ghi raw (vẫn được)
                print("⚠️ Kết quả không phải JSON line, ghi raw để postprocess xử lý.")
                out_lines.append(json_text.replace("\n", " "))
            else:
                out_lines.append(json.dumps(obj, ensure_ascii=False))
        else:
            # 1 dòng – cố gắng check JSON hợp lệ, nếu không hợp lệ vẫn ghi raw
            try:
                obj = json.loads(json_text)
            except Exception:
                print("⚠️ Kết quả không parse được JSON, ghi raw line.")
                out_lines.append(json_text)
            else:
                out_lines.append(json.dumps(obj, ensure_ascii=False))

    # Ghi file
    if out_lines:
        OUTPUT_FILE.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        print(f"\n✅ Đã ghi {len(out_lines)} dòng vào {OUTPUT_FILE}")
    else:
        print("⚠️ Không có dòng nào được ghi vào output_prompts.txt")


if __name__ == "__main__":
    main()
