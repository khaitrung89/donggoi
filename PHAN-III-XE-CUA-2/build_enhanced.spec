# -*- mode: python ; coding: utf-8 -*-
# Build spec cho FilmAI v2.0 Enhanced Edition

import sys
import os
from pathlib import Path

# Đường dẫn thư mục hiện tại (SPECPATH được định nghĩa bởi PyInstaller)
current_dir = Path(SPECPATH).absolute()

# Danh sách file data cần include
data_files = [
    ('camera_styles.txt', '.'),
    ('character_dictionary.json', '.'),
    ('extras_worlds.json', '.'),
    ('layer_rules.py', '.'),
    ('layer_filters.py', '.'),
    ('generate_prompts.py', '.'),
    ('translate_prompts.py', '.'),
    ('license_manager.py', '.'),
]

# File mẫu (optional)
optional_files = [
    ('api_keys.txt', '.'),
    ('scenes.txt', '.'),
    ('scenes_test.txt', '.'),
    ('README_V2.md', '.'),
]

# Thêm optional files nếu tồn tại
for file_path, dest in optional_files:
    full_path = current_dir / file_path
    if full_path.exists():
        data_files.append((file_path, dest))

block_cipher = None

a = Analysis(
    ['gui_app_enhanced.py'],  # File GUI mới
    pathex=[str(current_dir)],
    binaries=[],
    datas=data_files,
    hiddenimports=[
        'google.generativeai',
        'google.generativeai.types',
        'google.generativeai.client',
        'google.generativeai.models',
        'layer_rules',
        'layer_filters',
        'license_manager',
        'generate_prompts',
        'translate_prompts',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FilmAI-PromptGenerator-v2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Không hiện console (GUI app)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Có thể thêm icon.ico nếu muốn
)
