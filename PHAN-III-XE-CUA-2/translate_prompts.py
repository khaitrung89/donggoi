import google.generativeai as gen
import json
from pathlib import Path

# ==============================
# CẤU HÌNH FILE
# ==============================

API_KEYS_FILE = "api_keys.txt"
INPUT_FILE = "output_prompts_clean.txt"   # đầu vào sau postprocess
OUT_EN_FILE = "final_prompts_en.txt"      # copy bản EN
OUT_VI_FILE = "final_prompts_vi.txt"      # bản đã dịch sang tiếng Việt


# ==============================
# LOAD API KEYS (dùng chung với generate_prompts.py)
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
# PROMPT DỊCH JSON EN → VI
# ==============================

TRANSLATE_PROMPT = r"""
You are a professional bilingual translator (English → Vietnamese).

You receive ONE SINGLE JSON object (a film scene prompt) as plain text.

YOUR TASK:
- Translate ALL natural-language contents from English into Vietnamese.
- KEEP THE JSON STRUCTURE IDENTICAL.
- DO NOT change:
  * JSON keys
  * numeric values
  * "scene_number"
  * "cinematic.shot_type"
  * "cinematic.pov"
  * "cinematic.focus_characters"
  * character names like LANA, ADAI, ASUKA, LANA2, ADAI2, ASUKA2
- Only translate the string values of:
  * scene_title
  * scene_summary
  * character.emotions.primary
  * character.emotions.secondary
  * character.voice_tone
  * cinematic.camera
  * cinematic.lighting
  * cinematic.environment
  * cinematic.movement
  * dialogue.characters[*].line
  * action_block.length (you may translate or keep as is, both OK)
  * action_block.content

STYLE:
- Vietnamese must be natural, cinematic, giàu hình ảnh, không dịch word-by-word.
- Giữ đúng ngôi xưng (I → tôi, you → bạn / người, we → chúng ta, v.v. tùy ngữ cảnh).
- Không được thêm, bớt hoặc giải thích ngoài JSON.

OUTPUT RULES:
- OUTPUT ONLY the translated JSON.
- Do NOT wrap in ``` or any other text.
- Keep it on ONE SINGLE LINE.

JSON INPUT:
{json_str}
"""


# ==============================
# GỌI GEMINI DỊCH
# ==============================

def call_gemini(prompt: str) -> str:
    global current_key_index
    for _ in range(len(API_KEYS)):
        try:
            model = gen.GenerativeModel("models/gemini-2.5-flash")
            resp = model.generate_content(prompt)
            text = (resp.text or "").strip()

            # Nếu model bọc trong ``` ``` thì bỏ ra
            if text.startswith("```"):
                text = text.replace("```", "").strip()

            # Ép về 1 dòng
            text = " ".join(text.split())

            # Kiểm tra có phải JSON hợp lệ không
            json.loads(text)

            return text
        except Exception as e:
            print(f"⚠️ Lỗi với key #{current_key_index + 1}: {e}")
            print("🔄 Đang đổi sang API key tiếp theo...")
            switch_key()

    raise Exception("❌ Tất cả API key đều lỗi hoặc hết quota trong call_gemini().")


# ==============================
# MAIN
# ==============================

def main():
    in_path = Path(INPUT_FILE)
    if not in_path.exists():
        raise FileNotFoundError(f"Không tìm thấy {INPUT_FILE}")

    lines = [ln.strip() for ln in in_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    total = len(lines)
    print(f"📚 Đang dịch {total} prompt từ {INPUT_FILE} → {OUT_VI_FILE}")

    out_en = Path(OUT_EN_FILE).open("w", encoding="utf-8")
    out_vi = Path(OUT_VI_FILE).open("w", encoding="utf-8")

    for idx, line in enumerate(lines, start=1):
        print(f"⏳ Dịch prompt {idx}/{total}...")

        # Ghi bản tiếng Anh y nguyên (clean) để lưu trữ
        out_en.write(line + "\n")

        # Gọi model dịch sang tiếng Việt
        prompt = TRANSLATE_PROMPT.format(json_str=line)
        translated = call_gemini(prompt)

        out_vi.write(translated + "\n")

    out_en.close()
    out_vi.close()

    print(f"✅ Xong! Đã lưu {total} dòng vào {OUT_EN_FILE} (EN) và {OUT_VI_FILE} (VI).")


if __name__ == "__main__":
    main()
