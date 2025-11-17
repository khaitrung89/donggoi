import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import sys
import os
from pathlib import Path
import subprocess
import shutil
import json

# Import các module chính của tool
from license_manager import check_license, request_license

class SettingsDialog:
    """Dialog để cấu hình API Keys, World Type, Model, và Output"""

    def __init__(self, parent, config):
        self.result = None
        self.config = config.copy()  # Copy để không ảnh hưởng config gốc nếu Cancel

        # Tạo dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("⚙️ Cài đặt - Settings")
        self.dialog.geometry("700x550")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Tạo notebook (tabs)
        self.notebook = ttk.Notebook(self.dialog)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tạo các tabs
        self.create_api_keys_tab()
        self.create_config_tab()
        self.create_output_tab()

        # Nút Save/Cancel
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
        """Tab quản lý API Keys"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔑 API Keys")

        # Label hướng dẫn
        info_frame = ttk.Frame(tab)
        info_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(info_frame,
                text="📝 Nhập các Gemini API Keys (mỗi key một dòng):",
                font=("Arial", 10, "bold")).pack(anchor=tk.W)

        tk.Label(info_frame,
                text="Lấy API key tại: https://aistudio.google.com/apikey",
                font=("Arial", 9), fg="blue", cursor="hand2").pack(anchor=tk.W)

        # Text area cho API keys
        text_frame = ttk.Frame(tab)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.api_keys_text = tk.Text(text_frame, height=12, width=60,
                                     font=("Consolas", 9),
                                     yscrollcommand=scrollbar.set)
        self.api_keys_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.api_keys_text.yview)

        # Load keys hiện tại
        current_keys = self.config.get('api_keys', [])
        self.api_keys_text.insert('1.0', '\n'.join(current_keys))

        # Buttons
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        ttk.Button(btn_frame, text="📋 Paste từ Clipboard",
                  command=self.paste_from_clipboard).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="🗑️ Xóa tất cả",
                  command=self.clear_api_keys).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="✅ Kiểm tra Keys",
                  command=self.validate_api_keys).pack(side=tk.LEFT)

        # Status label
        self.api_status_label = tk.Label(tab, text="", font=("Arial", 9))
        self.api_status_label.pack(padx=10, pady=(0, 10))

    def create_config_tab(self):
        """Tab cấu hình World Type và Model"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Cấu hình")

        # World Type
        world_frame = ttk.LabelFrame(tab, text="🌍 World Type (Thể loại thế giới)", padding=10)
        world_frame.pack(fill=tk.X, padx=10, pady=10)

        self.world_type_var = tk.StringVar(value=self.config.get('world_type', 'modern'))

        ttk.Radiobutton(world_frame, text="🏙️ Modern (Hiện đại)",
                       variable=self.world_type_var, value="modern").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(world_frame, text="🏰 Medieval (Trung cổ)",
                       variable=self.world_type_var, value="medieval").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(world_frame, text="✨ Fantasy (Phép thuật)",
                       variable=self.world_type_var, value="fantasy").pack(anchor=tk.W, pady=2)

        # Model Selection
        model_frame = ttk.LabelFrame(tab, text="🤖 AI Model", padding=10)
        model_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.model_var = tk.StringVar(value=self.config.get('model', 'gemini-2.5-flash'))

        ttk.Radiobutton(model_frame, text="⚡ Gemini 2.5 Flash (Nhanh, rẻ)",
                       variable=self.model_var, value="gemini-2.5-flash").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(model_frame, text="🚀 Gemini 2.5 Flash-8B (Nhanh nhất)",
                       variable=self.model_var, value="gemini-2.5-flash-8b").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(model_frame, text="💎 Gemini 2.0 Flash Exp (Thử nghiệm)",
                       variable=self.model_var, value="gemini-2.0-flash-exp").pack(anchor=tk.W, pady=2)

        # Additional Settings
        other_frame = ttk.LabelFrame(tab, text="🔧 Tùy chọn khác", padding=10)
        other_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.auto_translate_var = tk.BooleanVar(value=self.config.get('auto_translate', True))
        ttk.Checkbutton(other_frame, text="Tự động dịch sang tiếng Việt sau khi generate",
                       variable=self.auto_translate_var).pack(anchor=tk.W, pady=2)

        self.open_output_var = tk.BooleanVar(value=self.config.get('open_output', False))
        ttk.Checkbutton(other_frame, text="Tự động mở file output sau khi hoàn thành",
                       variable=self.open_output_var).pack(anchor=tk.W, pady=2)

    def create_output_tab(self):
        """Tab cấu hình Output"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📁 Output")

        # Output directory
        dir_frame = ttk.LabelFrame(tab, text="📂 Thư mục lưu kết quả", padding=10)
        dir_frame.pack(fill=tk.X, padx=10, pady=10)

        self.output_dir_var = tk.StringVar(value=self.config.get('output_dir', str(Path.cwd())))

        entry_frame = ttk.Frame(dir_frame)
        entry_frame.pack(fill=tk.X)

        ttk.Entry(entry_frame, textvariable=self.output_dir_var,
                 font=("Arial", 9)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(entry_frame, text="📁 Chọn",
                  command=self.browse_output_dir).pack(side=tk.RIGHT)

        # File names
        files_frame = ttk.LabelFrame(tab, text="📝 Tên file output", padding=10)
        files_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # JSON output
        ttk.Label(files_frame, text="JSON output (Node 2):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.json_output_var = tk.StringVar(value=self.config.get('json_output', 'output_prompts.txt'))
        ttk.Entry(files_frame, textvariable=self.json_output_var, width=40).grid(row=0, column=1, padx=(5, 0), pady=5)

        # English output
        ttk.Label(files_frame, text="English output:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.en_output_var = tk.StringVar(value=self.config.get('en_output', 'final_prompts_en.txt'))
        ttk.Entry(files_frame, textvariable=self.en_output_var, width=40).grid(row=1, column=1, padx=(5, 0), pady=5)

        # Vietnamese output
        ttk.Label(files_frame, text="Vietnamese output:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.vi_output_var = tk.StringVar(value=self.config.get('vi_output', 'final_prompts_vi.txt'))
        ttk.Entry(files_frame, textvariable=self.vi_output_var, width=40).grid(row=2, column=1, padx=(5, 0), pady=5)

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
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tất cả API keys?"):
            self.api_keys_text.delete('1.0', tk.END)
            self.api_status_label.config(text="🗑️ Đã xóa tất cả", fg="orange")

    def validate_api_keys(self):
        """Kiểm tra format API keys"""
        text = self.api_keys_text.get('1.0', tk.END).strip()
        if not text:
            self.api_status_label.config(text="⚠️ Chưa có API key nào", fg="orange")
            return

        lines = [line.strip() for line in text.split('\n') if line.strip()]
        valid_count = 0

        for line in lines:
            # Basic validation: Gemini API keys thường bắt đầu với AIza
            if line.startswith('AIza') and len(line) > 30:
                valid_count += 1

        self.api_status_label.config(
            text=f"✅ Tìm thấy {valid_count}/{len(lines)} keys hợp lệ",
            fg="green" if valid_count == len(lines) else "orange"
        )

    def browse_output_dir(self):
        """Chọn thư mục output"""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)

    def save_settings(self):
        """Lưu settings"""
        # Get API keys
        text = self.api_keys_text.get('1.0', tk.END).strip()
        api_keys = [line.strip() for line in text.split('\n') if line.strip()]

        if not api_keys:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ít nhất 1 API key!")
            return

        # Update config
        self.config['api_keys'] = api_keys
        self.config['world_type'] = self.world_type_var.get()
        self.config['model'] = self.model_var.get()
        self.config['auto_translate'] = self.auto_translate_var.get()
        self.config['open_output'] = self.open_output_var.get()
        self.config['output_dir'] = self.output_dir_var.get()
        self.config['json_output'] = self.json_output_var.get()
        self.config['en_output'] = self.en_output_var.get()
        self.config['vi_output'] = self.vi_output_var.get()

        self.result = self.config
        self.dialog.destroy()

    def cancel(self):
        """Hủy"""
        self.result = None
        self.dialog.destroy()

    def show(self):
        """Hiển thị dialog và chờ kết quả"""
        self.dialog.wait_window()
        return self.result


class PromptGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FilmAI Prompt Generator - Premium Tool v2.0")
        self.root.geometry("900x650")
        self.root.resizable(True, True)

        # Cấu hình style
        self.setup_styles()

        # Load hoặc khởi tạo config
        self.load_config()

        # Biến lưu trữ
        self.input_file = tk.StringVar()
        self.is_running = False
        self.process = None

        # Kiểm tra license trước khi tạo giao diện
        if not self.check_license_first():
            root.destroy()
            sys.exit(1)

        # Tạo giao diện
        self.create_widgets()

    def load_config(self):
        """Load config từ file hoặc tạo mới"""
        config_file = Path("config.json")

        default_config = {
            'api_keys': [],
            'world_type': 'modern',
            'model': 'gemini-2.5-flash',
            'auto_translate': True,
            'open_output': False,
            'output_dir': str(Path.cwd()),
            'json_output': 'output_prompts.txt',
            'en_output': 'final_prompts_en.txt',
            'vi_output': 'final_prompts_vi.txt'
        }

        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                # Merge với default nếu thiếu keys
                for key, value in default_config.items():
                    if key not in self.config:
                        self.config[key] = value
            except:
                self.config = default_config
        else:
            self.config = default_config

        # Load API keys từ api_keys.txt nếu config chưa có
        if not self.config['api_keys']:
            api_keys_file = Path("api_keys.txt")
            if api_keys_file.exists():
                keys = [line.strip() for line in api_keys_file.read_text(encoding='utf-8').splitlines() if line.strip()]
                self.config['api_keys'] = keys

    def save_config(self):
        """Lưu config ra file"""
        try:
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)

            # Cũng lưu API keys ra api_keys.txt để tương thích với code cũ
            with open("api_keys.txt", 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.config['api_keys']))

        except Exception as e:
            print(f"Lỗi lưu config: {e}")

    def setup_styles(self):
        """Cấu hình style cho giao diện"""
        style = ttk.Style()

        # Màu sắc chính
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2196F3"
        self.success_color = "#4CAF50"
        self.error_color = "#f44336"

        self.root.configure(bg=self.bg_color)

    def check_license_first(self):
        """Kiểm tra license khi khởi động"""
        if not check_license():
            # Tạo cửa sổ license riêng
            license_window = tk.Toplevel(self.root)
            license_window.title("Kích hoạt bản quyền")
            license_window.geometry("500x300")
            license_window.transient(self.root)
            license_window.grab_set()

            # Label thông báo
            tk.Label(license_window, text="🔐 KÍCH HOẠT BẢN QUYỀN",
                    font=("Arial", 16, "bold")).pack(pady=20)

            tk.Label(license_window, text="Vui lòng nhập key bản quyền theo định dạng:",
                    font=("Arial", 10)).pack()

            tk.Label(license_window, text="XXXX-XXXX-XXXX-XXXX",
                    font=("Arial", 12, "bold"), fg="blue").pack(pady=5)

            # Entry cho license key
            key_entry = tk.Entry(license_window, font=("Arial", 12), width=25)
            key_entry.pack(pady=10)

            result_label = tk.Label(license_window, text="", font=("Arial", 10))
            result_label.pack(pady=5)

            def validate_license():
                key = key_entry.get().strip().upper()
                if not key:
                    result_label.config(text="❌ Vui lòng nhập key!", fg=self.error_color)
                    return

                # Gọi hàm request_license từ license_manager
                if request_license():
                    result_label.config(text="✅ Kích hoạt thành công!", fg=self.success_color)
                    license_window.after(1500, license_window.destroy)
                    return True
                else:
                    result_label.config(text="❌ Key không hợp lệ! Vui lòng thử lại.", fg=self.error_color)
                    key_entry.delete(0, tk.END)
                    return False

            # Nút xác nhận
            tk.Button(license_window, text="Kích hoạt",
                     command=validate_license,
                     bg=self.primary_color, fg="white",
                     font=("Arial", 11, "bold")).pack(pady=10)

            # Chờ cửa sổ license đóng
            self.root.wait_window(license_window)

            # Kiểm tra lại license sau khi đóng cửa sổ
            return check_license()

        return True

    def create_widgets(self):
        """Tạo các widget cho giao diện"""
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # Tiêu đề
        title_label = tk.Label(main_frame, text="🎬 FilmAI Prompt Generator v2.0",
                              font=("Arial", 20, "bold"), fg=self.primary_color)
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Frame chọn file input
        input_frame = ttk.LabelFrame(main_frame, text="📥 File Input (scenes.txt)", padding=10)
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)

        ttk.Entry(input_frame, textvariable=self.input_file, width=60).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10))
        ttk.Button(input_frame, text="📁 Chọn file", command=self.browse_input_file).grid(row=0, column=2, padx=(0, 10))

        # Mặc định chọn file scenes.txt nếu tồn tại
        default_file = Path("scenes.txt")
        if default_file.exists():
            self.input_file.set(str(default_file.absolute()))

        # Frame output directory
        output_frame = ttk.LabelFrame(main_frame, text="📤 Thư mục Output", padding=10)
        output_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)

        self.output_dir_label = tk.Label(output_frame, text=self.config['output_dir'],
                                         font=("Arial", 9), anchor=tk.W)
        self.output_dir_label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10)

        # Frame nút điều khiển
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, pady=(0, 15))

        # Nút Settings
        ttk.Button(control_frame, text="⚙️ Settings",
                  command=self.show_settings).pack(side=tk.LEFT, padx=(0, 10))

        # Nút start
        self.start_button = ttk.Button(control_frame, text="🚀 Bắt đầu Generate",
                                      command=self.start_generation)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))

        # Nút dừng
        self.stop_button = ttk.Button(control_frame, text="⏹️ Dừng",
                                     command=self.stop_generation,
                                     state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))

        # Nút xem kết quả
        self.view_result_button = ttk.Button(control_frame, text="📄 Mở thư mục Output",
                                           command=self.open_output_folder,
                                           state=tk.NORMAL)
        self.view_result_button.pack(side=tk.LEFT)

        # Frame hiển thị log
        log_frame = ttk.LabelFrame(main_frame, text="📋 Tiến trình chạy", padding=10)
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        # Text area cho log
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80,
                                                 font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Thanh trạng thái
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)

        self.status_label = ttk.Label(status_frame, text="✅ Sẵn sàng",
                                     font=("Arial", 10, "italic"))
        self.status_label.grid(row=0, column=0, sticky=tk.W)

        # Nút thoát
        ttk.Button(status_frame, text="❌ Thoát",
                  command=self.on_closing).grid(row=0, column=1, sticky=tk.E)

        # Bind sự kiện đóng cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Hiển thị config info
        self.update_config_display()

    def show_settings(self):
        """Hiển thị Settings dialog"""
        dialog = SettingsDialog(self.root, self.config)
        result = dialog.show()

        if result:
            self.config = result
            self.save_config()
            self.update_config_display()
            self.log_message("✅ Đã lưu settings mới")

    def update_config_display(self):
        """Cập nhật hiển thị config"""
        self.output_dir_label.config(text=f"📁 {self.config['output_dir']}")
        api_count = len(self.config.get('api_keys', []))
        world = self.config.get('world_type', 'modern')
        model = self.config.get('model', 'gemini-2.5-flash')

        info = f"🔑 {api_count} API keys | 🌍 {world.capitalize()} | 🤖 {model}"
        if hasattr(self, 'status_label'):
            self.status_label.config(text=info)

    def browse_input_file(self):
        """Chọn file input"""
        filename = filedialog.askopenfilename(
            title="Chọn file scenes.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)

    def log_message(self, message):
        """Thêm message vào log area"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def update_status(self, status):
        """Cập nhật trạng thái"""
        self.status_label.config(text=status)
        self.root.update_idletasks()

    def start_generation(self):
        """Bắt đầu generate prompts"""
        input_file = self.input_file.get()

        # Validate
        if not input_file:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file input!")
            return

        if not Path(input_file).exists():
            messagebox.showerror("Lỗi", f"File không tồn tại: {input_file}")
            return

        if not self.config.get('api_keys'):
            messagebox.showerror("Lỗi", "Chưa có API keys! Vui lòng vào Settings để thêm API keys.")
            return

        # Cập nhật giao diện
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.log_message("=" * 60)
        self.log_message("🚀 BẮT ĐẦU GENERATE PROMPTS")
        self.log_message("=" * 60)
        self.update_status("⏳ Đang chạy...")

        # Chạy trong thread riêng
        thread = threading.Thread(target=self.run_workflow)
        thread.daemon = True
        thread.start()

    def run_workflow(self):
        """Chạy workflow: Node 2 (generate) + Node 3 (translate)"""
        try:
            # Prepare scenes.txt
            input_file = self.input_file.get()
            original_scenes = Path("scenes.txt")
            backup_name = Path("scenes_backup.txt")

            # Backup và copy file
            if original_scenes.exists() and str(original_scenes.absolute()) != input_file:
                shutil.move(str(original_scenes), str(backup_name))

            if str(Path(input_file).absolute()) != str(original_scenes.absolute()):
                shutil.copy2(input_file, str(original_scenes))

            # === NODE 2: GENERATE PROMPTS ===
            self.log_message("\n📝 NODE 2: Generating JSON prompts...")
            self.log_message(f"   World Type: {self.config['world_type']}")
            self.log_message(f"   Model: {self.config['model']}")
            self.log_message(f"   API Keys: {len(self.config['api_keys'])} keys")

            # Update generate_prompts.py với config
            self.update_generate_script_config()

            # Run generate_prompts
            import generate_prompts
            generate_prompts.main()

            self.log_message("✅ Node 2 hoàn thành!")

            # === NODE 3: TRANSLATE (nếu enabled) ===
            if self.config.get('auto_translate', True):
                self.log_message("\n🌐 NODE 3: Translating to Vietnamese...")

                import translate_prompts
                translate_prompts.main()

                self.log_message("✅ Node 3 hoàn thành!")

            # Move outputs to configured directory
            self.move_outputs_to_directory()

            self.log_message("\n" + "=" * 60)
            self.log_message("🎉 HOÀN TẤT TẤT CẢ!")
            self.log_message("=" * 60)
            self.update_status("✅ Hoàn thành")

            # Open output nếu enabled
            if self.config.get('open_output', False):
                self.open_output_folder()

        except Exception as e:
            self.log_message(f"\n❌ LỖI: {e}")
            self.update_status("❌ Lỗi")
            import traceback
            self.log_message(traceback.format_exc())

        finally:
            # Restore files
            self.restore_files()

            # Cập nhật giao diện
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def update_generate_script_config(self):
        """Cập nhật config cho generate_prompts.py"""
        # Tạo file temp config
        temp_config = {
            'WORLD_TYPE': self.config['world_type'],
            'MODEL': self.config['model']
        }

        with open('_temp_config.json', 'w', encoding='utf-8') as f:
            json.dump(temp_config, f)

    def move_outputs_to_directory(self):
        """Di chuyển output files sang thư mục đã chọn"""
        output_dir = Path(self.config['output_dir'])

        # Tạo thư mục nếu chưa tồn tại
        output_dir.mkdir(parents=True, exist_ok=True)

        files_to_move = [
            ('output_prompts.txt', self.config['json_output']),
            ('final_prompts_en.txt', self.config['en_output']),
            ('final_prompts_vi.txt', self.config['vi_output'])
        ]

        for src_name, dst_name in files_to_move:
            src = Path(src_name)
            if src.exists():
                dst = output_dir / dst_name
                shutil.copy2(str(src), str(dst))
                self.log_message(f"📁 Saved: {dst}")

    def restore_files(self):
        """Khôi phục lại các file gốc"""
        try:
            original_scenes = Path("scenes.txt")
            backup_name = Path("scenes_backup.txt")

            # Khôi phục file backup nếu có
            if backup_name.exists():
                if original_scenes.exists():
                    original_scenes.unlink()
                shutil.move(str(backup_name), str(original_scenes))

        except Exception as e:
            self.log_message(f"⚠️ Cảnh báo: {e}")

    def stop_generation(self):
        """Dừng quá trình generate"""
        if self.is_running:
            self.log_message("⏹️ Đang dừng...")
            self.update_status("⏹️ Đang dừng...")
            self.is_running = False

    def open_output_folder(self):
        """Mở thư mục output"""
        output_dir = self.config['output_dir']
        try:
            if os.name == 'nt':  # Windows
                os.startfile(output_dir)
            elif sys.platform == 'darwin':  # Mac
                subprocess.call(['open', output_dir])
            else:  # Linux
                subprocess.call(['xdg-open', output_dir])
        except Exception as e:
            self.log_message(f"❌ Không thể mở thư mục: {e}")

    def on_closing(self):
        """Xử lý khi đóng cửa sổ"""
        if self.is_running:
            if messagebox.askokcancel("Xác nhận", "Tool đang chạy. Bạn có chắc muốn thoát?"):
                self.restore_files()
                self.save_config()
                self.root.destroy()
        else:
            self.save_config()
            self.root.destroy()


def main():
    """Hàm chính để chạy GUI"""
    root = tk.Tk()
    app = PromptGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
