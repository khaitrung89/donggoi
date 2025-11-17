# layer_rules.py
# Chứa các RULES quan trọng để nhét vào PROMPT_TEMPLATE cho model
# Bao gồm: cast chính, nhân vật phụ không tên, giới hạn vai trò.

CORE_RULES = """
CORE CAST RULES (VERY IMPORTANT):
- The ONLY named main characters you are allowed to use are: Alex, Maya, Marcus.
- You MUST NOT invent new named characters (such as Kael, Ava, John, etc.).
- Any additional people must be described as unnamed roles only, for example:
  "a young maid", "a middle-aged porter", "a palace guard",
  "a forest fairy", "a wounded villager", "two temple monks", etc.
- These secondary characters must NEVER be given personal names.

- The MAIN physical actions, emotional beats, and camera focus must always belong to
  Alex, Maya, or Marcus. Background characters can assist, react, or be affected,
  but must NOT replace them in key actions or heroic moments.

DIALOGUE RULES:
- In "dialogue.characters", every "speaker" MUST be one of:
  "Alex", "Maya", or "Marcus".
- Secondary/background characters are NOT allowed to speak in the JSON structure
  (they can be described acting or reacting in the action_block, but must not be
  listed as "speaker").

FOCUS & CLOSE-UP RULES:
- In "cinematic.focus_characters", every name MUST be one of:
  "Alex", "Maya", "Marcus", or their close-up forms "Alex2", "Maya2", "Marcus2".
- Secondary characters MUST NOT be placed inside "focus_characters".
- If shot_type is "close-up" or "extreme close-up", the focus characters must be:
  Alex2, Maya2, Marcus2 (or a combination of them).
- If shot_type is "wide" or "medium", the focus characters must be:
  Alex, Maya, Marcus (or a combination of them).

SECONDARY CHARACTER (EXTRAS) RULES:
- You may introduce unnamed secondary characters based on the provided world extras:
  for example palace maids, castle soldiers, forest fairies, villagers, office workers…
- Every secondary character must be described with clear ROLE + APPEARANCE, such as:
  "a young maid in pastel robes with braided hair and timid eyes",
  "a muscular porter in coarse linen with a shaved head",
  "a forest fairy with glowing wings and long silver hair".
- These secondary characters:
  * MUST remain unnamed (no personal names).
  * MAY reappear across multiple scenes with consistent role and appearance.
  * SHOULD NOT appear in more than approximately 4 scenes in total,
    so they never overshadow the main trio.
  * If a secondary character is clearly described as dying in the story,
    you MUST treat them as gone and not bring them back in later scenes.

- Secondary characters MUST NOT:
  * Lead the main plot.
  * Replace Alex, Maya, or Marcus in emotional climaxes.
  * Take over the heroic resolution of the scene.

WORLD CONTEXT FOR SECONDARY CHARACTERS:
- You will be given a short description of typical secondary characters for the current world
  (modern, medieval, or fantasy). You MUST choose secondary roles that fit that world only.
- Do NOT mix settings. For example:
  * In medieval scenes, do NOT spawn "office workers" or "taxi drivers".
  * In modern scenes, do NOT spawn "temple monks in ancient robes" or "palace maids".
  * In fantasy scenes, you MAY combine magical beings (fairies, sages, spirits) with
    more grounded roles (villagers, guards) as long as the tone is consistent.
"""
