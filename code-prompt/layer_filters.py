# layer_filters.py
# Chứa các hàm hậu xử lý JSON:
# - close-up rename (Alex -> Alex2...)
# - lọc nhân vật lạ ra khỏi focus_characters & dialogue.speaker

from typing import Dict, Any, Set

ALLOWED_BASE_NAMES: Set[str] = {"Alex", "Maya", "Marcus"}


def apply_closeup_name_switch(data: Dict[str, Any], character_dict: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    """
    Nếu shot_type là close-up / extreme close-up:
      - focus_characters: Alex -> Alex2, Maya -> Maya2, Marcus -> Marcus2
        (dùng name_closeup từ character_dict nếu có, fallback name+'2').
    Nếu không phải close-up thì giữ nguyên.
    """
    cinematic = data.get("cinematic", {}) or {}
    shot_type = str(cinematic.get("shot_type", "")).strip().lower().replace(" ", "").replace("-", "")
    is_closeup = shot_type in ("closeup", "extremecloseup")

    if not is_closeup:
        return data

    focus = cinematic.get("focus_characters")
    if not isinstance(focus, list):
        return data

    new_focus = []
    for name in focus:
        if isinstance(name, str):
            if name in character_dict:
                close_name = character_dict[name].get("name_closeup", name + "2")
                new_focus.append(close_name)
            else:
                # fallback nếu không có trong character_dict
                new_focus.append(name + "2")
        else:
            new_focus.append(name)

    cinematic["focus_characters"] = new_focus
    data["cinematic"] = cinematic
    return data


def enforce_allowed_characters(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    - Loại bỏ / chỉnh sửa những nhân vật không nằm trong ALLOWED_BASE_NAMES
      ở:
        + cinematic.focus_characters
        + dialogue.characters[].speaker

    - Nếu gặp tên lạ (vd: "Kael", "Ava"), sẽ:
        + Bỏ ra khỏi focus_characters
        + Bỏ câu thoại có speaker lạ

    => Nhân vật phụ chỉ tồn tại trong phần mô tả (action_block),
       KHÔNG tồn tại như một speaker hay focus explicit trong JSON.
    """
    # ---- FOCUS CHARACTERS ----
    cinematic = data.get("cinematic", {}) or {}
    focus = cinematic.get("focus_characters")

    if isinstance(focus, list):
        new_focus = []
        for name in focus:
            if not isinstance(name, str):
                continue
            base = _base_name(name)
            if base in ALLOWED_BASE_NAMES:
                new_focus.append(name)
            else:
                print(f"⚠ Removed illegal focus character: {name}")
        cinematic["focus_characters"] = new_focus
        data["cinematic"] = cinematic

    # ---- DIALOGUE SPEAKERS ----
    dlg = data.get("dialogue", {}) or {}
    chars = dlg.get("characters")

    if isinstance(chars, list):
        new_chars = []
        for item in chars:
            if not isinstance(item, dict):
                continue
            speaker = item.get("speaker", "")
            if not isinstance(speaker, str):
                continue
            base = _base_name(speaker)
            if base in ALLOWED_BASE_NAMES:
                new_chars.append(item)
            else:
                print(f"⚠ Removed dialogue line with illegal speaker: {speaker}")
        dlg["characters"] = new_chars
        data["dialogue"] = dlg

    return data


def _base_name(name: str) -> str:
    """
    Lấy 'gốc' của tên:
      - Alex2 -> Alex
      - Maya10 -> Maya
      - Marcus -> Marcus
    """
    i = len(name)
    while i > 0 and name[i - 1].isdigit():
        i -= 1
    return name[:i] if i > 0 else name
