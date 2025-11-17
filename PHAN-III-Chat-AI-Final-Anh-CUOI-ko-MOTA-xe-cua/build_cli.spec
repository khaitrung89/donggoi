# -*- mode: python ; coding: utf-8 -*-
# Build spec cho command-line version (không dùng GUI)

import sys
import os
from pathlib import Path

# Đường dẫn thư mục hiện tại (SPECPATH được định nghĩa bởi PyInstaller)
current_dir = Path(SPECPATH).absolute()

# Danh sách file data cần include (các file .txt, .json)
data_files = [
    ('api_keys.txt', '.'),
    ('camera_styles.txt', '.'),
    ('character_dictionary.json', '.'),
    ('extras_worlds.json', '.'),
    ('scenes.txt', '.'),
]

# Kiểm tra và thêm các file nếu tồn tại
for file_path, dest in data_files[:]:
    full_path = current_dir / file_path
    if not full_path.exists():
        data_files.remove((file_path, dest))

block_cipher = None

a = Analysis(
    ['generate_prompts.py'],  # CLI version - không cần GUI
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
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'PyQt5', 'PySide2'],  # Loại bỏ GUI libraries
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
    name='FilmAI-CLI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console app
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
