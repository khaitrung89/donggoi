#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI ĐẦY ĐỦ 5 BƯỚC cho XE-CUA-2 FilmAI Tool
=========================================

WORKFLOW:
[0] story_idea.txt → form nhập hoặc import
[1] generate_chapters_from_idea.py → chapters.txt
[2] generate_scenes_from_chapters.py → scenes.txt (chọn số cảnh)
[3] generate_prompts.py → output_prompts.txt
[4] postprocess_output_prompts.py → output_prompts_clean.txt
[5] translate_prompts.py → final_prompts_en.txt + final_prompts_vi.txt

Author: Claude AI Enhanced Edition
Version: 2.0 Full Workflow
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import sys
import os
from pathlib import Path
import subprocess
import shutil
import json
import google.generativeai as gen

# Import các module chính
from license_manager import check_license, request_license

# =========================
# SETTINGS DIALOG
# =========================

class SettingsDialog:
    """Dialog để cấu hình API Keys, World Type, Model, và Output"""

    def __init__(self, parent, config):
        self.result = None
        self.config = config.copy()

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("⚙️ Cài đặt - Settings")
        self.dialog.geometry("700x550")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.dialog)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_api_keys_tab()
        self.create_config_tab()
        self.create_output_tab()

        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        ttk.Button(button_frame, text="💾 Lưu",
                  command=self.save_settings).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="❌ Hủy",
                  command=self.cancel).pack(side=tk.RIGHT)

        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")

    def create_api_keys_tab(self):
        """Tab 1: API Keys"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔑 API Keys")

        info_frame = ttk.Frame(tab)
        info_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(info_frame,
                text="📝 Nhập các Gemini API Keys (mỗi key một dòng):",
                font=("Arial", 10, "bold")).pack(anchor=tk.W)

        tk.Label(info_frame,
                text="Lấy API key tại: https://aistudio.google.com/apikey",
                font=("Arial", 9), fg="blue").pack(anchor=tk.W)

        # Text area
        text_frame = ttk.Frame(tab)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.api_keys_text = tk.Text(text_frame, height=12, width=60,
                                     font=("Consolas", 9),
                                     yscrollcommand=scrollbar.set)
        self.api_keys_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.api_keys_text.yview)

        # Load current keys
        current_keys = self.config.get('api_keys', [])
        self.api_keys_text.insert('1.0', '\n'.join(current_keys))

        # Buttons
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        ttk.Button(btn_frame, text="📋 Paste từ Clipboard",
                  command=self.paste_from_clipboard).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="🗑️ Xóa tất cả",
                  command=self.clear_api_keys).pack(side=tk.LEFT)

        # Status
        self.api_status_label = tk.Label(tab, text="", font=("Arial", 9))
        self.api_status_label.pack(padx=10, pady=(0, 10))

    def create_config_tab(self):
        """Tab 2: Configuration"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Configuration")

        # World Type
        world_frame = ttk.LabelFrame(tab, text="🌍 World Type", padding=10)
        world_frame.pack(fill=tk.X, padx=10, pady=10)

        self.world_var = tk.StringVar(value=self.config.get('world_type', 'medieval'))

        ttk.Radiobutton(world_frame, text="🏰 Medieval (Fantasy)",
                       variable=self.world_var, value="medieval").pack(anchor=tk.W)
        ttk.Radiobutton(world_frame, text="🏙️ Modern (City)",
                       variable=self.world_var, value="modern").pack(anchor=tk.W)
        ttk.Radiobutton(world_frame, text="✨ Fantasy (Magic)",
                       variable=self.world_var, value="fantasy").pack(anchor=tk.W)

        # Model Selection
        model_frame = ttk.LabelFrame(tab, text="🤖 AI Model", padding=10)
        model_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.model_var = tk.StringVar(value=self.config.get('model', 'gemini-2.5-flash'))

        models = [
            ("Gemini 2.5 Flash (Nhanh, Rẻ)", "gemini-2.5-flash"),
            ("Gemini Flash-8B (Siêu nhanh)", "gemini-flash-8b"),
            ("Gemini 2.0 Flash Exp (Thử nghiệm)", "gemini-2.0-flash-exp")
        ]

        for label, value in models:
            ttk.Radiobutton(model_frame, text=label,
                           variable=self.model_var, value=value).pack(anchor=tk.W)

        # Chapter Settings
        chapter_frame = ttk.LabelFrame(tab, text="📖 Chapter Settings", padding=10)
        chapter_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(chapter_frame, text="Số chương mong muốn:").pack(anchor=tk.W)

        chapter_subframe = ttk.Frame(chapter_frame)
        chapter_subframe.pack(fill=tk.X, pady=5)

        tk.Label(chapter_subframe, text="Min:").pack(side=tk.LEFT)
        self.min_chapters_var = tk.IntVar(value=self.config.get('min_chapters', 6))
        ttk.Spinbox(chapter_subframe, from_=3, to=20, width=5,
                   textvariable=self.min_chapters_var).pack(side=tk.LEFT, padx=5)

        tk.Label(chapter_subframe, text="Max:").pack(side=tk.LEFT, padx=(10, 0))
        self.max_chapters_var = tk.IntVar(value=self.config.get('max_chapters', 12))
        ttk.Spinbox(chapter_subframe, from_=3, to=30, width=5,
                   textvariable=self.max_chapters_var).pack(side=tk.LEFT, padx=5)

    def create_output_tab(self):
        """Tab 3: Output Settings"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📁 Output")

        # Output directory
        dir_frame = ttk.LabelFrame(tab, text="📂 Thư mục lưu kết quả", padding=10)
        dir_frame.pack(fill=tk.X, padx=10, pady=10)

        self.output_dir_var = tk.StringVar(value=self.config.get('output_dir', str(Path.cwd())))

        dir_entry_frame = ttk.Frame(dir_frame)
        dir_entry_frame.pack(fill=tk.X, pady=5)

        ttk.Entry(dir_entry_frame, textvariable=self.output_dir_var,
                 state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(dir_entry_frame, text="📁 Chọn",
                  command=self.browse_output_dir).pack(side=tk.LEFT, padx=(5, 0))

        # File naming
        naming_frame = ttk.LabelFrame(tab, text="📝 Tên file output", padding=10)
        naming_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        entries = [
            ("JSON Output:", 'json_output', 'output_prompts.txt'),
            ("Clean JSON:", 'clean_output', 'output_prompts_clean.txt'),
            ("English:", 'en_output', 'final_prompts_en.txt'),
            ("Vietnamese:", 'vi_output', 'final_prompts_vi.txt')
        ]

        self.output_vars = {}
        for label, key, default in entries:
            row = ttk.Frame(naming_frame)
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=label, width=15, anchor=tk.W).pack(side=tk.LEFT)
            var = tk.StringVar(value=self.config.get(key, default))
            ttk.Entry(row, textvariable=var).pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.output_vars[key] = var

        # Auto-open output
        self.auto_open_var = tk.BooleanVar(value=self.config.get('auto_open', False))
        ttk.Checkbutton(tab, text="✅ Tự động mở thư mục output sau khi hoàn tất",
                       variable=self.auto_open_var).pack(padx=10, pady=10, anchor=tk.W)

    def paste_from_clipboard(self):
        """Paste API keys từ clipboard"""
        try:
            clipboard_text = self.dialog.clipboard_get()
            self.api_keys_text.delete('1.0', tk.END)
            self.api_keys_text.insert('1.0', clipboard_text)
            self.api_status_label.config(text="✅ Đã paste từ clipboard", fg="green")
        except:
            self.api_status_label.config(text="❌ Clipboard trống hoặc lỗi", fg="red")

    def clear_api_keys(self):
        """Xóa tất cả API keys"""
        self.api_keys_text.delete('1.0', tk.END)
        self.api_status_label.config(text="🗑️ Đã xóa tất cả keys", fg="orange")

    def browse_output_dir(self):
        """Chọn thư mục output"""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)

    def save_settings(self):
        """Lưu settings"""
        # Parse API keys
        keys_text = self.api_keys_text.get('1.0', tk.END).strip()
        api_keys = [line.strip() for line in keys_text.splitlines() if line.strip()]

        if not api_keys:
            messagebox.showerror("Lỗi", "Phải có ít nhất 1 API key!")
            return

        # Build config
        self.config['api_keys'] = api_keys
        self.config['world_type'] = self.world_var.get()
        self.config['model'] = self.model_var.get()
        self.config['min_chapters'] = self.min_chapters_var.get()
        self.config['max_chapters'] = self.max_chapters_var.get()
        self.config['output_dir'] = self.output_dir_var.get()
        self.config['auto_open'] = self.auto_open_var.get()

        for key, var in self.output_vars.items():
            self.config[key] = var.get()

        self.result = self.config
        self.dialog.destroy()

    def cancel(self):
        """Hủy"""
        self.result = None
        self.dialog.destroy()

    def show(self):
        """Hiển thị dialog và đợi"""
        self.dialog.wait_window()
        return self.result

# =========================
# MAIN APPLICATION
# =========================

class FilmAIApp:
    """Main GUI Application với đầy đủ 5 bước workflow"""

    def __init__(self, root):
        self.root = root
        self.root.title("🎬 XE-CUA-2 FilmAI Tool - Full Workflow v2.0")
        self.root.geometry("900x750")

        # Load config
        self.config = self.load_config()

        # API key rotation
        self.current_key_index = 0

        # Build UI
        self.create_menu()
        self.create_story_idea_section()
        self.create_workflow_section()
        self.create_log_section()
        self.create_status_bar()

        # License check on startup
        self.root.after(500, self.check_license_on_startup)

    def load_config(self):
        """Load config từ file hoặc tạo mới"""
        config_file = Path("config.json")

        default_config = {
            'api_keys': [],
            'world_type': 'medieval',
            'model': 'gemini-2.5-flash',
            'min_chapters': 6,
            'max_chapters': 12,
            'output_dir': str(Path.cwd()),
            'json_output': 'output_prompts.txt',
            'clean_output': 'output_prompts_clean.txt',
            'en_output': 'final_prompts_en.txt',
            'vi_output': 'final_prompts_vi.txt',
            'auto_open': False
        }

        if config_file.exists():
            try:
                loaded = json.loads(config_file.read_text(encoding='utf-8'))
                default_config.update(loaded)
            except:
                pass

        # Backward compatibility: load từ api_keys.txt nếu có
        if not default_config['api_keys']:
            api_keys_file = Path("api_keys.txt")
            if api_keys_file.exists():
                keys = [line.strip() for line in api_keys_file.read_text(encoding='utf-8').splitlines() if line.strip()]
                default_config['api_keys'] = keys

        return default_config

    def save_config(self):
        """Lưu config vào file"""
        config_file = Path("config.json")
        config_file.write_text(json.dumps(self.config, indent=2, ensure_ascii=False), encoding='utf-8')

        # Cũng save vào api_keys.txt cho backward compatibility
        api_keys_file = Path("api_keys.txt")
        api_keys_file.write_text('\n'.join(self.config['api_keys']), encoding='utf-8')

    def create_menu(self):
        """Tạo menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 File", menu=file_menu)
        file_menu.add_command(label="⚙️ Settings", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Exit", command=self.root.quit)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Help", menu=help_menu)
        help_menu.add_command(label="📖 Hướng dẫn", command=self.show_help)
        help_menu.add_command(label="ℹ️ About", command=self.show_about)

    def create_story_idea_section(self):
        """Section nhập Story Idea"""
        frame = ttk.LabelFrame(self.root, text="📝 BƯỚC 0: Story Idea (Ý tưởng phim)", padding=10)
        frame.pack(fill=tk.BOTH, padx=10, pady=10)

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(btn_frame, text="📂 Import từ file .txt",
                  command=self.import_story_idea).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="💾 Lưu story_idea.txt",
                  command=self.save_story_idea).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="🗑️ Xóa",
                  command=self.clear_story_idea).pack(side=tk.LEFT, padx=(5, 0))

        # Text area
        self.story_text = scrolledtext.ScrolledText(frame, height=8, width=80,
                                                    font=("Consolas", 9), wrap=tk.WORD)
        self.story_text.pack(fill=tk.BOTH, expand=True)

        # Load existing story_idea.txt nếu có
        story_file = Path("story_idea.txt")
        if story_file.exists():
            self.story_text.insert('1.0', story_file.read_text(encoding='utf-8'))

    def create_workflow_section(self):
        """Section 5 bước workflow"""
        frame = ttk.LabelFrame(self.root, text="🎬 WORKFLOW - 5 BƯỚC", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Scene count selector (cho Step 2)
        scene_frame = ttk.Frame(frame)
        scene_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(scene_frame, text="📊 Số cảnh cho Step 2:",
                font=("Arial", 9, "bold")).pack(side=tk.LEFT)

        self.scene_count_var = tk.IntVar(value=70)
        ttk.Radiobutton(scene_frame, text="~40 (Compact)",
                       variable=self.scene_count_var, value=40).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(scene_frame, text="~70 (Standard)",
                       variable=self.scene_count_var, value=70).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(scene_frame, text="~100 (Epic)",
                       variable=self.scene_count_var, value=100).pack(side=tk.LEFT, padx=5)

        tk.Label(scene_frame, text="Custom:").pack(side=tk.LEFT, padx=(10, 0))
        self.custom_scene_var = tk.IntVar(value=70)
        ttk.Spinbox(scene_frame, from_=20, to=200, width=5,
                   textvariable=self.custom_scene_var,
                   command=lambda: self.scene_count_var.set(self.custom_scene_var.get())).pack(side=tk.LEFT, padx=5)

        # Workflow buttons (2 cột)
        workflow_grid = ttk.Frame(frame)
        workflow_grid.pack(fill=tk.X, pady=(0, 10))

        # Column 1: Steps 1-3
        col1 = ttk.Frame(workflow_grid)
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        ttk.Button(col1, text="1️⃣ Generate Chapters",
                  command=self.run_step1).pack(fill=tk.X, pady=2)
        ttk.Button(col1, text="2️⃣ Generate Scenes",
                  command=self.run_step2).pack(fill=tk.X, pady=2)
        ttk.Button(col1, text="3️⃣ Generate Prompts",
                  command=self.run_step3).pack(fill=tk.X, pady=2)

        # Column 2: Steps 4-5
        col2 = ttk.Frame(workflow_grid)
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Button(col2, text="4️⃣ Postprocess Clean",
                  command=self.run_step4).pack(fill=tk.X, pady=2)
        ttk.Button(col2, text="5️⃣ Translate EN/VI",
                  command=self.run_step5).pack(fill=tk.X, pady=2)

        # Start from selector
        start_frame = ttk.Frame(frame)
        start_frame.pack(fill=tk.X, pady=(5, 0))

        tk.Label(start_frame, text="🚀 Chạy từ bước:",
                font=("Arial", 9, "bold")).pack(side=tk.LEFT)

        self.start_step_var = tk.IntVar(value=1)
        for i in range(1, 6):
            ttk.Radiobutton(start_frame, text=f"Step {i}",
                           variable=self.start_step_var, value=i).pack(side=tk.LEFT, padx=5)

        ttk.Button(start_frame, text="▶️ Chạy toàn bộ từ bước đã chọn",
                  command=self.run_from_step,
                  style="Accent.TButton").pack(side=tk.RIGHT, padx=(10, 0))

    def create_log_section(self):
        """Section hiển thị log"""
        frame = ttk.LabelFrame(self.root, text="📋 LOG", padding=5)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.log_text = scrolledtext.ScrolledText(frame, height=15, width=80,
                                                  font=("Consolas", 8),
                                                  bg="#1e1e1e", fg="#d4d4d4",
                                                  wrap=tk.WORD, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Configure tags for colored output
        self.log_text.tag_config("info", foreground="#4ec9b0")
        self.log_text.tag_config("success", foreground="#6a9955")
        self.log_text.tag_config("error", foreground="#f48771")
        self.log_text.tag_config("warning", foreground="#dcdcaa")

    def create_status_bar(self):
        """Status bar"""
        self.status_var = tk.StringVar(value="✅ Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var,
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def log_message(self, message, tag="info"):
        """Ghi log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def check_license_on_startup(self):
        """Kiểm tra license khi khởi động"""
        if not check_license():
            self.log_message("❌ License không hợp lệ hoặc chưa kích hoạt", "error")
            response = messagebox.askyesno(
                "License Required",
                "Bạn cần kích hoạt license để sử dụng tool.\n\nKích hoạt ngay?"
            )
            if response:
                self.activate_license()
            else:
                self.root.quit()
        else:
            self.log_message("✅ License hợp lệ", "success")

    def activate_license(self):
        """Kích hoạt license"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🔐 Kích hoạt License")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Nhập License Key:", font=("Arial", 10, "bold")).pack(pady=10)

        entry = ttk.Entry(dialog, width=40, font=("Consolas", 10))
        entry.pack(pady=5)
        entry.focus()

        def submit():
            key = entry.get().strip()
            if request_license(key):
                messagebox.showinfo("Thành công", "✅ License đã được kích hoạt!")
                self.log_message("✅ License activated successfully", "success")
                dialog.destroy()
            else:
                messagebox.showerror("Lỗi", "❌ License key không hợp lệ!")

        ttk.Button(dialog, text="✅ Kích hoạt", command=submit).pack(pady=10)

        dialog.bind('<Return>', lambda e: submit())

    def open_settings(self):
        """Mở Settings dialog"""
        settings_dialog = SettingsDialog(self.root, self.config)
        result = settings_dialog.show()

        if result:
            self.config = result
            self.save_config()
            self.log_message("✅ Settings đã được lưu", "success")

            # Reload API keys
            self.current_key_index = 0
            if self.config['api_keys']:
                self.set_current_api_key()

    def set_current_api_key(self):
        """Set API key hiện tại"""
        if not self.config['api_keys']:
            raise ValueError("❌ Chưa cấu hình API keys!")

        api_key = self.config['api_keys'][self.current_key_index]
        gen.configure(api_key=api_key)
        self.log_message(f"🔑 Đang dùng API key #{self.current_key_index + 1}/{len(self.config['api_keys'])}", "info")

    def switch_api_key(self):
        """Chuyển sang API key tiếp theo"""
        self.current_key_index = (self.current_key_index + 1) % len(self.config['api_keys'])
        self.set_current_api_key()

    def import_story_idea(self):
        """Import story_idea.txt"""
        file_path = filedialog.askopenfilename(
            title="Chọn file Story Idea",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                content = Path(file_path).read_text(encoding='utf-8')
                self.story_text.delete('1.0', tk.END)
                self.story_text.insert('1.0', content)
                self.log_message(f"✅ Đã import: {file_path}", "success")
            except Exception as e:
                self.log_message(f"❌ Lỗi import: {e}", "error")

    def save_story_idea(self):
        """Lưu story_idea.txt"""
        content = self.story_text.get('1.0', tk.END).strip()
        if not content:
            messagebox.showwarning("Cảnh báo", "Story idea đang trống!")
            return

        try:
            Path("story_idea.txt").write_text(content, encoding='utf-8')
            self.log_message("✅ Đã lưu story_idea.txt", "success")
        except Exception as e:
            self.log_message(f"❌ Lỗi lưu file: {e}", "error")

    def clear_story_idea(self):
        """Xóa story idea"""
        if messagebox.askyesno("Xác nhận", "Xóa toàn bộ nội dung Story Idea?"):
            self.story_text.delete('1.0', tk.END)
            self.log_message("🗑️ Đã xóa Story Idea", "warning")

    # =============================
    # WORKFLOW STEPS
    # =============================

    def run_step1(self):
        """Step 1: Generate Chapters"""
        self.save_story_idea()  # Tự động lưu trước
        threading.Thread(target=self._run_step1_thread, daemon=True).start()

    def _run_step1_thread(self):
        """Thread cho Step 1"""
        try:
            self.log_message("=" * 60, "info")
            self.log_message("1️⃣ STEP 1: Generating Chapters from Idea...", "info")
            self.status_var.set("⏳ Step 1: Generating chapters...")

            # Check story_idea.txt
            if not Path("story_idea.txt").exists():
                self.log_message("❌ Không tìm thấy story_idea.txt", "error")
                self.status_var.set("❌ Error: story_idea.txt not found")
                return

            idea_text = Path("story_idea.txt").read_text(encoding='utf-8').strip()
            if not idea_text:
                self.log_message("❌ File story_idea.txt đang trống", "error")
                self.status_var.set("❌ Error: story_idea.txt empty")
                return

            # Set API key
            self.set_current_api_key()

            # Build prompt
            from generate_chapters_from_idea import CHAPTER_PROMPT_TEMPLATE
            prompt = CHAPTER_PROMPT_TEMPLATE.format(
                min_chapters=self.config['min_chapters'],
                max_chapters=self.config['max_chapters'],
                idea_text=idea_text
            )

            # Call Gemini
            self.log_message("🤖 Calling Gemini AI...", "info")
            chapters_text = self.call_gemini_with_retry(prompt)

            # Save output
            Path("chapters.txt").write_text(chapters_text, encoding='utf-8')

            self.log_message("✅ Step 1 hoàn tất: chapters.txt", "success")
            self.status_var.set("✅ Step 1 completed")

        except Exception as e:
            self.log_message(f"❌ Lỗi Step 1: {e}", "error")
            self.status_var.set(f"❌ Step 1 failed: {e}")

    def run_step2(self):
        """Step 2: Generate Scenes"""
        threading.Thread(target=self._run_step2_thread, daemon=True).start()

    def _run_step2_thread(self):
        """Thread cho Step 2"""
        try:
            self.log_message("=" * 60, "info")
            self.log_message("2️⃣ STEP 2: Generating Scenes from Chapters...", "info")
            self.status_var.set("⏳ Step 2: Generating scenes...")

            # Check chapters.txt
            if not Path("chapters.txt").exists():
                self.log_message("❌ Không tìm thấy chapters.txt (chạy Step 1 trước)", "error")
                self.status_var.set("❌ Error: chapters.txt not found")
                return

            chapters_text = Path("chapters.txt").read_text(encoding='utf-8').strip()
            if not chapters_text:
                self.log_message("❌ File chapters.txt đang trống", "error")
                return

            # Get scene count
            total_scenes = self.scene_count_var.get()
            if total_scenes == 0:  # Custom
                total_scenes = self.custom_scene_var.get()

            scenes_per_chapter = max(1, total_scenes // 12)

            # Detail level
            if total_scenes <= 45:
                detail_level = "concise but still cinematic"
            elif total_scenes <= 85:
                detail_level = "rich cinematic detail and clear beats"
            else:
                detail_level = "very detailed, multi-step cinematic sequences"

            self.log_message(f"📊 Tổng số cảnh: {total_scenes} ({scenes_per_chapter} cảnh/chapter)", "info")
            self.log_message(f"📝 Detail level: {detail_level}", "info")

            # Set API key
            self.set_current_api_key()

            # Build prompt
            from generate_scenes_from_chapters import SCENE_SPLIT_PROMPT_TEMPLATE
            prompt = SCENE_SPLIT_PROMPT_TEMPLATE.format(
                min_scenes=scenes_per_chapter,
                max_scenes=scenes_per_chapter,
                detail_level=detail_level,
                chapters_text=chapters_text
            )

            # Call Gemini
            self.log_message("🤖 Calling Gemini AI...", "info")
            scenes_text = self.call_gemini_with_retry(prompt)

            # Save output
            Path("scenes.txt").write_text(scenes_text.strip(), encoding='utf-8')

            self.log_message("✅ Step 2 hoàn tất: scenes.txt", "success")
            self.status_var.set("✅ Step 2 completed")

        except Exception as e:
            self.log_message(f"❌ Lỗi Step 2: {e}", "error")
            self.status_var.set(f"❌ Step 2 failed: {e}")

    def run_step3(self):
        """Step 3: Generate Prompts"""
        threading.Thread(target=self._run_step3_thread, daemon=True).start()

    def _run_step3_thread(self):
        """Thread cho Step 3"""
        try:
            self.log_message("=" * 60, "info")
            self.log_message("3️⃣ STEP 3: Generating Super JSON Prompts...", "info")
            self.status_var.set("⏳ Step 3: Generating prompts...")

            # Import và chạy generate_prompts
            import generate_prompts
            generate_prompts.main()

            self.log_message("✅ Step 3 hoàn tất: output_prompts.txt", "success")
            self.status_var.set("✅ Step 3 completed")

        except Exception as e:
            self.log_message(f"❌ Lỗi Step 3: {e}", "error")
            self.status_var.set(f"❌ Step 3 failed: {e}")

    def run_step4(self):
        """Step 4: Postprocess"""
        threading.Thread(target=self._run_step4_thread, daemon=True).start()

    def _run_step4_thread(self):
        """Thread cho Step 4"""
        try:
            self.log_message("=" * 60, "info")
            self.log_message("4️⃣ STEP 4: Postprocessing (Normalize & Clean)...", "info")
            self.status_var.set("⏳ Step 4: Postprocessing...")

            # Import và chạy postprocess
            import postprocess_output_prompts
            postprocess_output_prompts.main()

            self.log_message("✅ Step 4 hoàn tất: output_prompts_clean.txt", "success")
            self.status_var.set("✅ Step 4 completed")

        except Exception as e:
            self.log_message(f"❌ Lỗi Step 4: {e}", "error")
            self.status_var.set(f"❌ Step 4 failed: {e}")

    def run_step5(self):
        """Step 5: Translate"""
        threading.Thread(target=self._run_step5_thread, daemon=True).start()

    def _run_step5_thread(self):
        """Thread cho Step 5"""
        try:
            self.log_message("=" * 60, "info")
            self.log_message("5️⃣ STEP 5: Translating to Vietnamese...", "info")
            self.status_var.set("⏳ Step 5: Translating...")

            # Import và chạy translate
            import translate_prompts
            translate_prompts.main()

            # Copy files đến output directory
            self.move_outputs_to_directory()

            self.log_message("✅ Step 5 hoàn tất: final_prompts_en.txt + final_prompts_vi.txt", "success")
            self.status_var.set("✅ All steps completed!")

            # Auto open output directory
            if self.config.get('auto_open', False):
                output_dir = Path(self.config['output_dir'])
                if output_dir.exists():
                    if sys.platform == 'win32':
                        os.startfile(str(output_dir))
                    elif sys.platform == 'darwin':
                        subprocess.run(['open', str(output_dir)])
                    else:
                        subprocess.run(['xdg-open', str(output_dir)])

        except Exception as e:
            self.log_message(f"❌ Lỗi Step 5: {e}", "error")
            self.status_var.set(f"❌ Step 5 failed: {e}")

    def run_from_step(self):
        """Chạy toàn bộ workflow từ bước đã chọn"""
        start_step = self.start_step_var.get()
        self.log_message(f"🚀 Bắt đầu workflow từ Step {start_step}...", "warning")

        steps = {
            1: self.run_step1,
            2: self.run_step2,
            3: self.run_step3,
            4: self.run_step4,
            5: self.run_step5
        }

        # Run sequentially (simplified - in production would chain callbacks)
        threading.Thread(target=lambda: self._run_workflow_from(start_step), daemon=True).start()

    def _run_workflow_from(self, start_step):
        """Chạy workflow tuần tự từ bước start_step"""
        import time

        step_methods = [
            None,  # index 0 (không dùng)
            self._run_step1_thread,
            self._run_step2_thread,
            self._run_step3_thread,
            self._run_step4_thread,
            self._run_step5_thread
        ]

        for step in range(start_step, 6):
            self.log_message(f"\n{'='*60}", "info")
            self.log_message(f"▶️ Đang chạy Step {step}...", "warning")

            try:
                step_methods[step]()
                time.sleep(2)  # Wait for completion
            except Exception as e:
                self.log_message(f"❌ Workflow dừng tại Step {step}: {e}", "error")
                return

        self.log_message(f"\n{'='*60}", "success")
        self.log_message("🎉 HOÀN TẤT TOÀN BỘ WORKFLOW!", "success")
        self.status_var.set("🎉 All workflow completed!")

    def move_outputs_to_directory(self):
        """Copy output files sang thư mục đã chọn"""
        output_dir = Path(self.config['output_dir'])

        # Tạo thư mục nếu chưa tồn tại
        output_dir.mkdir(parents=True, exist_ok=True)

        files_to_move = [
            ('output_prompts.txt', self.config['json_output']),
            ('output_prompts_clean.txt', self.config['clean_output']),
            ('final_prompts_en.txt', self.config['en_output']),
            ('final_prompts_vi.txt', self.config['vi_output'])
        ]

        for src_name, dst_name in files_to_move:
            src = Path(src_name)
            if src.exists():
                dst = output_dir / dst_name
                shutil.copy2(str(src), str(dst))
                self.log_message(f"📁 Saved: {dst}", "success")

    def call_gemini_with_retry(self, prompt):
        """Call Gemini với auto-retry khi lỗi API key"""
        for _ in range(len(self.config['api_keys'])):
            try:
                model = gen.GenerativeModel(f"models/{self.config['model']}")
                resp = model.generate_content(prompt)
                text = (resp.text or "").strip()

                # Remove code fences nếu có
                if text.startswith("```"):
                    text = text.replace("```", "").strip()

                return text

            except Exception as e:
                self.log_message(f"⚠️ Lỗi với API key #{self.current_key_index + 1}: {e}", "warning")
                self.log_message("🔄 Đổi sang API key tiếp theo...", "warning")
                self.switch_api_key()

        raise Exception("❌ Tất cả API key đều lỗi hoặc hết quota!")

    def show_help(self):
        """Hiển thị help"""
        help_text = """
🎬 XE-CUA-2 FilmAI Tool - Full Workflow v2.0

WORKFLOW 5 BƯỚC:
────────────────
Step 0: Nhập Story Idea (form hoặc import .txt)
Step 1: Generate Chapters (story_idea.txt → chapters.txt)
Step 2: Generate Scenes (chapters.txt → scenes.txt)
Step 3: Generate Prompts (scenes.txt → output_prompts.txt)
Step 4: Postprocess (output_prompts.txt → output_prompts_clean.txt)
Step 5: Translate (output_prompts_clean.txt → final_prompts_en/vi.txt)

CÁCH DÙNG:
──────────
1. Cấu hình Settings (API Keys, Model, Output)
2. Nhập Story Idea (hoặc import từ file)
3. Chọn số cảnh cho Step 2 (40/70/100 hoặc custom)
4. Chạy từng bước hoặc "Chạy toàn bộ"
5. Nhận file final_prompts_en.txt + final_prompts_vi.txt

TROUBLESHOOTING:
────────────────
- API key invalid → Kiểm tra lại tại Settings
- File không tìm thấy → Chạy step trước đó
- Workflow dừng → Xem log để biết lỗi

📖 Đọc thêm: README_V2.md, HUONG_DAN_TAI_VA_SU_DUNG.md
        """
        messagebox.showinfo("Help", help_text)

    def show_about(self):
        """Hiển thị about"""
        about_text = """
🎬 XE-CUA-2 FilmAI Tool
Full Workflow Edition v2.0

Công cụ tạo AI Video Prompts với Gemini AI
Hỗ trợ đầy đủ 5 bước từ ý tưởng đến Super JSON

Developed by: Claude AI
License: Commercial (require activation key)
Model: Gemini 2.5 Flash / Flash-8B / 2.0 Flash Exp

GitHub: khaitrung89/donggoi
        """
        messagebox.showinfo("About", about_text)

# =========================
# MAIN ENTRY POINT
# =========================

def main():
    root = tk.Tk()
    app = FilmAIApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
