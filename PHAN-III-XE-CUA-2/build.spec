# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Đường dẫn thư mục hiện tại
current_dir = Path(__file__).parent.absolute()

# Danh sách file data cần include (các file .txt, .json)
data_files = [
    ('api_keys.txt', '.'),
    ('camera_styles.txt', '.'),
    ('character_dictionary.json', '.'),
    ('extras_worlds.json', '.'),
    ('scenes.txt', '.'),
    ('CAC-GOC-CHUP.txt', '.'),
    ('README.md', '.'),
]

# Kiểm tra và thêm các file nếu tồn tại
for file_path, dest in data_files[:]:
    full_path = current_dir / file_path
    if not full_path.exists():
        data_files.remove((file_path, dest))

block_cipher = None

a = Analysis(
    ['gui_app.py'],  # File chính để chạy GUI
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
    name='FilmAI-PromptGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Ẩn console window (chỉ chạy GUI)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Có thể thêm icon.ico nếu có
)