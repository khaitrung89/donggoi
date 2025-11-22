import google.generativeai as gen
import json
import re
from pathlib import Path

# ==============================
# CẤU HÌNH TÊN FILE
# ==============================

API_KEYS_FILE = "api_keys.txt"
INPUT_FILE = "output_prompts.txt"          # JSON gốc từ generate_prompts.py (mỗi dòng 1 JSON)
OUTPUT_EN_FILE = "final_prompts_en.txt"    # Bản tiếng Anh
OUTPUT_VI_FILE = "final_prompts_vi.txt"    # Bản tiếng Việt


# ==============================
# 1. LOAD API KEYS
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
# 2. LOAD INPUT PROMPTS
# ==============================

def load_prompts(path: str = INPUT_FILE):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {path}")

    lines = [line.strip() for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    print(f"📚 Đã nạp {len(lines)} prompt từ {INPUT_FILE}")
    return lines


prompts = load_prompts()


# ==============================
# 3. PROMPT DỊCH → FULL TIẾNG VIỆT
# ==============================

TRANSLATE_PROMPT = """
You are a professional translator specializing in cinematic JSON prompts.

TASK:
Translate the following JSON object from ENGLISH to VIETNAMESE.

RULES:
1. Translate ALL string values into NATURAL, CINEMATIC VIETNAMESE.
   - This includes: scene_title, setting texts, camera, shot_type, lighting,
     mood, style, effects, sound, dialogue lines, action_block, appearance,
     voice_tone, and any other text fields.
2. DO NOT change any JSON keys, structure, or field order.
3. DO NOT add or remove any fields.
4. Character names (e.g. "Alex", "Maya", "Marcus", "Kael") MUST stay in English.
5. Return ONLY the translated JSON, on ONE SINGLE LINE.
6. Do NOT add explanations, comments, or Markdown code fences.

ORIGINAL JSON:
<<JSON>>
"""


# ==============================
# 4. HỖ TRỢ: XOÁ CODE BLOCK MARKDOWN
# ==============================

def clean_markdown_blocks(text: str) -> str:
    """Loại bỏ ```json ... ``` nếu model trả về dạng code block."""
    text = text.strip()
    if text.startswith("```"):
        # Xoá prefix ```... và tất cả dấu ``` còn lại
        text = re.sub(r"^```[a-zA-Z0-9]*", "", text)
        text = text.replace("```", "").strip()
    return text


# ==============================
# 5. GỌI GEMINI ĐỂ DỊCH
# ==============================

def translate_to_vietnamese(json_str: str) -> str:
    global current_key_index

    for _ in range(len(API_KEYS)):
        try:
            model = gen.GenerativeModel("models/gemini-2.5-flash")
            prompt = TRANSLATE_PROMPT.replace("<<JSON>>", json_str)
            resp = model.generate_content(prompt)

            raw_text = resp.text or ""
            text = clean_markdown_blocks(raw_text)
            one_line = " ".join(text.splitlines()).strip()

            # Thử parse JSON để đảm bảo vẫn là JSON hợp lệ
            try:
                json.loads(one_line)
            except Exception as e:
                print(f"⚠️ Cảnh báo: JSON dịch không parse được, vẫn ghi raw string. Lỗi: {e}")

            return one_line

        except Exception as e:
            print(f"⚠️ Key #{current_key_index + 1} lỗi: {e}")
            print("🔄 Đổi sang API key tiếp theo...")
            switch_key()

    raise Exception("❌ Tất cả API keys đều lỗi / hết quota.")


# ==============================
# 6. CLEAN 1 DÒNG JSON ĐẦU VÀO
# ==============================

def clean_json_line(line: str) -> str:
    """
    Làm sạch 1 dòng JSON:
    - Bỏ prefix 'English prompt:' nếu lỡ dính từ lần chạy cũ
    - Bỏ ```json / ``` nếu có
    - Ghép về 1 dòng duy nhất
    """
    s = line.strip()

    if s.startswith("English prompt:"):
        s = s.replace("English prompt:", "", 1).strip()

    s = clean_markdown_blocks(s)
    s = " ".join(s.splitlines()).strip()
    return s


# ==============================
# 7. MAIN
# ==============================

def main():
    if not prompts:
        print("⚠️ File input không có JSON.")
        return

    # Reset file output
    Path(OUTPUT_EN_FILE).write_text("", encoding="utf-8")
    Path(OUTPUT_VI_FILE).write_text("", encoding="utf-8")

    with Path(OUTPUT_EN_FILE).open("a", encoding="utf-8") as en_f, \
         Path(OUTPUT_VI_FILE).open("a", encoding="utf-8") as vi_f:

        for idx, raw_line in enumerate(prompts, start=1):
            print(f"⏳ Dịch prompt {idx}/{len(prompts)}...")

            # 1. Làm sạch & validate JSON tiếng Anh gốc
            clean_en = clean_json_line(raw_line)

            try:
                json.loads(clean_en)
            except Exception as e:
                print(f"⚠️ JSON input lỗi dòng {idx}: {e}")

            # 2. Ghi bản tiếng Anh: MỖI DÒNG = 1 JSON THUẦN
            en_f.write(clean_en + "\n")

            # 3. Dịch sang tiếng Việt
            try:
                vi_json = translate_to_vietnamese(clean_en)
                vi_f.write(vi_json + "\n")
            except Exception as e:
                print(f"❌ Lỗi dịch dòng {idx}: {e}")
                vi_f.write(json.dumps("[TRANSLATION ERROR]") + "\n")

    print(f"\n🎉 Hoàn tất dịch!")
    print(f"➡️ Bản tiếng Anh: {OUTPUT_EN_FILE}")
    print(f"➡️ Bản tiếng Việt: {OUTPUT_VI_FILE}")


if __name__ == "__main__":
    main()
