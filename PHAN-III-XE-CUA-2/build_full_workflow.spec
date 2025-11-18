# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec cho XE-CUA-2 FilmAI Tool - Full Workflow v2.0
================================================================
Build EXE từ gui_app_full_workflow.py với đầy đủ 5 bước workflow
"""

from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Sử dụng SPECPATH thay vì __file__ (PyInstaller compatible)
current_dir = Path(SPECPATH).absolute()

# Collect data files
data_files = [
    (str(current_dir / 'character_dictionary.json'), '.'),
    (str(current_dir / 'layer_rules.py'), '.'),
    (str(current_dir / 'layer_filters.py'), '.'),
    (str(current_dir / 'license_manager.py'), '.'),
    (str(current_dir / 'generate_chapters_from_idea.py'), '.'),
    (str(current_dir / 'generate_scenes_from_chapters.py'), '.'),
    (str(current_dir / 'generate_prompts.py'), '.'),
    (str(current_dir / 'postprocess_output_prompts.py'), '.'),
    (str(current_dir / 'translate_prompts.py'), '.'),
]

# Hidden imports
hiddenimports = [
    'google.generativeai',
    'google.ai',
    'google.ai.generativelanguage',
    'layer_rules',
    'layer_filters',
    'license_manager',
    'generate_chapters_from_idea',
    'generate_scenes_from_chapters',
    'generate_prompts',
    'postprocess_output_prompts',
    'translate_prompts',
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.scrolledtext',
    'tkinter.messagebox',
]

a = Analysis(
    ['gui_app_full_workflow.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=data_files,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='XE-CUA-2-FilmAI-FullWorkflow',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI mode (no console)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Thêm icon nếu có
)
