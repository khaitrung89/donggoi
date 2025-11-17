import json
from pathlib import Path

INPUT_FILE = "output_prompts.txt"
OUTPUT_FILE = "output_prompts_clean.txt"
CHARACTER_DICT_FILE = "character_dictionary.json"


def load_character_dict(path: str = CHARACTER_DICT_FILE):
    p = Path(path)
    if not p.exists():
        return {"LANA": {}, "ADAI": {}, "ASUKA": {}}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
        return {"LANA": {}, "ADAI": {}, "ASUKA": {}}
    except Exception:
        return {"LANA": {}, "ADAI": {}, "ASUKA": {}}


def build_name_maps(char_dict: dict):
    canonical_by_lower = {}
    for name in char_dict.keys():
        canonical_by_lower[name.lower()] = name.upper()
    return canonical_by_lower


def normalize_shot_type(raw: str) -> str:
    if not raw:
        return "medium"
    s = raw.strip().lower().replace("_", " ").replace("-", " ")
    if "extreme" in s and "close" in s:
        return "extreme close-up"
    if "close" in s:
        return "close-up"
    if "wide" in s:
        return "wide"
    if "medium" in s:
        return "medium"
    return "medium"


def normalize_pov(raw: str) -> str:
    if not raw:
        return "third_person"
    s = raw.strip().lower().replace("-", "_").replace(" ", "_")
    allowed = {"third_person", "over_shoulder", "first_person", "god_view"}
    if s in allowed:
        return s
    if s in {"thirdperson", "third"}:
        return "third_person"
    if s in {"firstperson", "first"}:
        return "first_person"
    if s in {"godview", "top_view", "top"}:
        return "god_view"
    return "third_person"


def normalize_emotion(value: str) -> str:
    if not value:
        return "none"
    v = value.strip()
    if v.lower() in {"none", "null", "n/a", "no"}:
        return "none"
    return v


def normalize_voice_tone(value: str) -> str:
    if not value:
        return "neutral"
    v = value.strip()
    if v.lower() in {"none", "null", "n/a", "no", "na"}:
        return "neutral"
    return v


def normalize_character_name(name: str, canonical_map: dict):
    if not name:
        return "NONE"
    n = name.strip()
    if not n or n.lower() in {"none", "no one", "no_one", "null"}:
        return "NONE"
    base = n.rstrip("2").strip()
    low = base.lower()
    if low in canonical_map:
        return canonical_map[low]
    return n


def try_parse_json_with_fallback(line: str):
    """
    1) Thử json.loads trực tiếp.
    2) Nếu lỗi, tìm đoạn từ { ... } trong line, parse lại.
    3) Nếu vẫn lỗi -> raise để caller quyết định.
    """
    line = line.strip()
    # Thử parse trực tiếp
    try:
        return json.loads(line)
    except Exception:
        pass

    # Thử tìm substring từ { đến } cuối cùng
    start = line.find("{")
    end = line.rfind("}")
    if start != -1 and end != -1 and end > start:
        sub = line[start:end+1]
        try:
            return json.loads(sub)
        except Exception:
            # Nếu vẫn lỗi, ném lỗi tiếp
            raise
    # Không tìm thấy {} hợp lệ
    raise ValueError("Không tìm thấy JSON substring hợp lệ trong dòng.")


def process_line(line: str, canonical_map: dict) -> str:
    try:
        data = try_parse_json_with_fallback(line)
    except Exception as e:
        print(f"⚠️ Không parse được JSON (kể cả fallback), giữ nguyên dòng. Lỗi: {e}")
        return line

    # 1) Character block
    char = data.get("character", {}) or {}
    name = char.get("name", "")
    char["name"] = normalize_character_name(name, canonical_map)

    emotions = char.get("emotions", {})
    if not isinstance(emotions, dict):
        emotions = {}
    emotions["primary"] = normalize_emotion(emotions.get("primary", ""))
    emotions["secondary"] = normalize_emotion(emotions.get("secondary", ""))
    char["emotions"] = emotions

    vt = char.get("voice_tone", "")
    char["voice_tone"] = normalize_voice_tone(vt)
    data["character"] = char

    # 2) Cinematic block
    cine = data.get("cinematic", {}) or {}
    shot_raw = cine.get("shot_type", "")
    shot_type = normalize_shot_type(shot_raw)
    cine["shot_type"] = shot_type

    pov_raw = cine.get("pov", "")
    cine["pov"] = normalize_pov(pov_raw)

    focus = cine.get("focus_characters", [])
    if not isinstance(focus, list):
        focus = []
    is_close = shot_type in {"close-up", "extreme close-up"}

    new_focus = []
    for item in focus:
        if not isinstance(item, str):
            new_focus.append(item)
            continue
        s = item.strip()
        base = s.rstrip("2").strip()
        low = base.lower()
        if low in canonical_map:
            base_canon = canonical_map[low]
            if is_close:
                new_focus.append(base_canon + "2")
            else:
                new_focus.append(base_canon)
        else:
            new_focus.append(s)
    cine["focus_characters"] = new_focus
    data["cinematic"] = cine

    # 3) Dialogue speakers
    dialog = data.get("dialogue", {}) or {}
    chars = dialog.get("characters", [])
    if isinstance(chars, list):
        for d in chars:
            if not isinstance(d, dict):
                continue
            sp = d.get("speaker", "")
            normalized = normalize_character_name(sp, canonical_map)
            if normalized == "NONE":
                normalized = ""
            d["speaker"] = normalized
    dialog["characters"] = chars
    data["dialogue"] = dialog

    return json.dumps(data, ensure_ascii=False)


def main():
    char_dict = load_character_dict()
    canonical_map = build_name_maps(char_dict)

    in_path = Path(INPUT_FILE)
    if not in_path.exists():
        print(f"❌ Không tìm thấy {INPUT_FILE}")
        return

    lines = [ln.rstrip("\n") for ln in in_path.read_text(encoding="utf-8").splitlines()]
    out_lines = []
    for i, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        print(f"🔧 Đang xử lý dòng {i}/{len(lines)}...")
        out_lines.append(process_line(line, canonical_map))

    Path(OUTPUT_FILE).write_text("\n".join(out_lines), encoding="utf-8")
    print(f"✅ Đã ghi {len(out_lines)} dòng chuẩn hóa vào {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
