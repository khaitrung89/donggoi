# ai_utils.py
from pathlib import Path
import time
from typing import List, Optional

import google.generativeai as genai

API_KEYS_FILE = Path("api_keys.txt")
DEFAULT_MODEL = "models/gemini-2.5-flash"


class NoValidAPIKeyError(Exception):
    """Ném ra khi tất cả API key đều lỗi/hết quota."""
    pass


def load_api_keys() -> List[str]:
    """Đọc danh sách API key (mỗi dòng 1 key) từ api_keys.txt."""
    if not API_KEYS_FILE.exists():
        raise FileNotFoundError("Không tìm thấy api_keys.txt")

    keys = [
        line.strip()
        for line in API_KEYS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not keys:
        raise ValueError("api_keys.txt không có key nào")
    return keys


def call_gemini_text(
    prompt: str,
    model_name: str = DEFAULT_MODEL,
    system_instruction: Optional[str] = None,
    max_retries_per_key: int = 2,
) -> str:
    """
    Gọi Gemini → trả về text.
    - Tự xoay API key khi hết quota / key die.
    - Nếu tất cả key lỗi → ném NoValidAPIKeyError.
    """

    keys = load_api_keys()
    last_error = None

    for idx, key in enumerate(keys, start=1):
        try:
            genai.configure(api_key=key)

            model = genai.GenerativeModel(
                model_name,
                system_instruction=system_instruction,
            )

            for attempt in range(max_retries_per_key):
                try:
                    resp = model.generate_content(prompt)

                    # SDK mới: resp.text thường có sẵn
                    if hasattr(resp, "text") and resp.text:
                        return resp.text.strip()

                    # fallback: lôi text từ candidates
                    candidates = getattr(resp, "candidates", None)
                    if candidates:
                        parts = candidates[0].content.parts
                        if parts and hasattr(parts[0], "text"):
                            return parts[0].text.strip()

                    raise RuntimeError("Phản hồi từ Gemini không có text hợp lệ.")
                except Exception as e:
                    last_error = e
                    msg = str(e).lower()

                    # lỗi key / quota → bỏ key này, qua key tiếp theo
                    if any(x in msg for x in [
                        "api key expired",
                        "api_key_invalid",
                        "permission_denied",
                        "rate limit",
                        "quota",
                    ]):
                        break

                    # lỗi tạm thời → chờ 1s rồi thử lại trên cùng key
                    time.sleep(1)

            # sang key tiếp theo
        except Exception as e:
            last_error = e
            continue

    raise NoValidAPIKeyError(
        f"Tất cả API key đều lỗi hoặc hết quota. Lỗi cuối: {last_error}"
    )


def normalize_to_english(raw_text: str) -> str:
    """
    Nhận input Việt/Anh/mix -> trả về bản tiếng Anh sạch, giữ cấu trúc.
    Dùng cho Zone 1 (story_idea) / Zone 2 nếu cần.
    """
    prompt = f"""
You are a professional screenwriting assistant.

The user will give you a story idea that may contain Vietnamese, English, or a mix of both.
Your task:

1. Understand the full meaning of the idea.
2. Rewrite it COMPLETELY IN ENGLISH.
3. Preserve the high-level structure (sections, headings, bullet points) if present.
4. Do NOT add new story elements that are not implied by the original idea.
5. Do NOT translate section labels like "ACT 1", "ACT 2", "ACT 3" if they are already in English.

Here is the original idea:

====================
{raw_text}
====================

Now respond ONLY with the English version.
"""
    return call_gemini_text(prompt)


def translate_en_to_vi_json(json_block: str) -> str:
    """
    Dịch 1 JSON từ EN → VI, giữ nguyên key + cấu trúc JSON.
    Dùng cho bước translate_prompts.
    """
    prompt = f"""
You are a JSON-preserving translator.

You will receive ONE JSON object in English.
Your tasks:

- Translate ALL natural-language content from English to Vietnamese.
- KEEP ALL JSON KEYS AS IS (do NOT translate key names).
- KEEP THE JSON STRUCTURE EXACTLY THE SAME.
- Only change the TEXT VALUES (strings) that are human-readable content.
- Preserve placeholders, camera codes, IDs, and technical flags as-is.

Return ONLY the translated JSON object, without explanation.

JSON INPUT:
{json_block}
"""
    return call_gemini_text(prompt)
