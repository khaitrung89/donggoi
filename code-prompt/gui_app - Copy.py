import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import sys
from pathlib import Path
import threading

# ===========================
# CONFIG
# ===========================
BASE_DIR = Path(__file__).resolve().parent
API_KEYS_FILE = BASE_DIR / "api_keys.txt"
STORY_IDEA = BASE_DIR / "story_idea.txt"


# ===========================
# SIMPLE DARK THEME
# ===========================
def apply_dark_theme(root: tk.Tk):
    """
    Dark mode đơn giản, KHÔNG dùng azure.tcl
    nên không cần file theme bên ngoài.
    """
    style = ttk.Style(root)
    # cố dùng 'clam', nếu không có thì thôi
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    bg = "#1e1e1e"
    fg = "#f0f0f0"
    btn_bg_active = "#3e3e3e"

    root.configure(bg=bg)

    style.configure(".", background=bg, foreground=fg)
    style.configure("TFrame", background=bg)
    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("TButton", padding=6)
    style.map(
        "TButton",
        background=[("active", btn_bg_active)],
        foreground=[("active", fg)],
    )


# ===========================
# GUI CLASS
# ===========================
class FilmAIGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Siêu Prompt Tool – Premium GUI")
        self.root.geometry("1200x720")

        apply_dark_theme(root)

        self.is_running = False
        self.api_error_shown = False

        self._build_layout()

    # ===========================
    # BUILD GUI
    # ===========================
    def _build_layout(self):
        root = self.root

        # ====== LEFT PANEL ======
        left = ttk.Frame(root)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(left, text="🔑 Gemini API Keys (1 dòng / key)").pack(anchor="w")
        self.api_text = tk.Text(left, height=12, width=35)
        self.api_text.pack(fill=tk.X)

        ttk.Button(left, text="💾 Save API Keys", command=self.save_api).pack(
            fill=tk.X, pady=5
        )
        ttk.Button(left, text="📂 Open story_idea.txt", command=self.open_story_idea).pack(
            fill=tk.X
        )

        ttk.Label(left, text=" ").pack()  # spacing

        # Buttons B0 ... B7
        self._build_step_buttons(left)

        # ====== RIGHT PANEL ======
        right = ttk.Frame(root)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_box = tk.Text(right, wrap="word")
        self.log_box.pack(fill=tk.BOTH, expand=True)

        # Status bar
        bottom = ttk.Frame(root)
        bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 8))

        self.status_label = ttk.Label(bottom, text="Sẵn sàng")
        self.status_label.pack(side=tk.LEFT)

        ttk.Button(
            bottom, text="🚀 Run B1→B6 (One-click)", command=self.run_full_pipeline
        ).pack(side=tk.RIGHT, padx=(0, 6))

        ttk.Button(bottom, text="🧹 Clear Log", command=self.clear_log).pack(
            side=tk.RIGHT, padx=(0, 6)
        )
        ttk.Button(bottom, text="❌ Thoát", command=self.on_close).pack(
            side=tk.RIGHT
        )

        # Load API keys
        self.load_api_keys()

    # ===========================
    # LEFT PANEL – BUTTON STEPS
    # ===========================
    def _build_step_buttons(self, panel):
        ttk.Label(panel, text="📘 Pipeline B0 → B7").pack(anchor="w", pady=(10, 3))

        steps = [
            ("B0 – Nhập Ý Tưởng (Form HTML)", self.b0_open_form),
            ("B1 – Mở story_idea.txt", self.open_story_idea),
            (
                "B2 – Generate CHAPTERS",
                lambda: self.run_script("generate_chapters_from_idea.py"),
            ),
            (
                "B3 – Generate SCENES",
                lambda: self.run_script("generate_scenes_from_chapters.py"),
            ),
            (
                "B4 – Generate PROMPTS",
                lambda: self.run_script("generate_prompts.py"),
            ),
            (
                "B5 – Postprocess PROMPTS",
                lambda: self.run_script("postprocess_output_prompts.py"),
            ),
            (
                "B6 – Translate EN → VI",
                lambda: self.run_script("translate_prompts.py"),
            ),
            ("B7 – Mở thư mục hiện tại", self.open_output_folder),
        ]

        for name, func in steps:
            ttk.Button(panel, text=name, command=func).pack(fill=tk.X, pady=2)

    # ===========================
    # STEP BUTTON FUNCTIONS
    # ===========================
    def b0_open_form(self):
        """Open story_idea_form.html"""
        html = BASE_DIR / "story_idea_form.html"
        if not html.exists():
            messagebox.showerror(
                "Không tìm thấy HTML",
                "Không tìm thấy file story_idea_form.html.\n"
                "Hãy đặt file này cùng thư mục với chương trình.",
            )
            return
        subprocess.Popen(["start", str(html)], shell=True)

    def open_story_idea(self):
        if not STORY_IDEA.exists():
            STORY_IDEA.write_text("", encoding="utf-8")
        subprocess.Popen(["notepad.exe", str(STORY_IDEA)])

    def open_output_folder(self):
        subprocess.Popen(["explorer", str(BASE_DIR)])

    # ===========================
    # RUN SCRIPT (1 STEP)
    # ===========================
    def run_script(self, script_name: str):
        """Run 1 step: python script.py"""
        if self.is_running:
            messagebox.showinfo("Đang chạy", "Đang có tiến trình khác chạy.")
            return

        script_path = BASE_DIR / script_name
        if not script_path.exists():
            self.log(f"❌ File không tồn tại: {script_name}")
            self.set_status(f"Thiếu {script_name}", ok=False)
            return

        self.is_running = True
        self.api_error_shown = False
        self.set_status(f"Đang chạy {script_name}", ok=None)

        def worker():
            try:
                proc = subprocess.Popen(
                    [sys.executable, str(script_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=str(BASE_DIR),
                )
                assert proc.stdout is not None

                for line in proc.stdout:
                    line = line.rstrip("\n")
                    if not line:
                        continue

                    # Detect API error
                    if "API key expired" in line or "API_KEY_INVALID" in line:
                        if not self.api_error_shown:
                            messagebox.showerror(
                                "API Key Error",
                                "API key bị lỗi hoặc hết hạn. Hãy kiểm tra lại api_keys.txt.",
                            )
                            self.api_error_shown = True

                    self.log(line)

                code = proc.wait()
                if code == 0:
                    self.set_status(f"{script_name} hoàn thành", ok=True)
                else:
                    self.set_status(f"{script_name} lỗi (exit {code})", ok=False)

            finally:
                self.is_running = False

        threading.Thread(target=worker, daemon=True).start()

    # ===========================
    # ONE-CLICK PIPELINE B2→B6
    # ===========================
    def run_full_pipeline(self):
        """Run B2→B6 in sequence (one-click)"""
        if not STORY_IDEA.exists():
            messagebox.showwarning(
                "Thiếu file",
                "story_idea.txt chưa có.\nHãy nhập B0 và bấm Lưu trước.",
            )
            return

        if not API_KEYS_FILE.exists() or not API_KEYS_FILE.read_text(
            encoding="utf-8"
        ).strip():
            messagebox.showwarning(
                "Thiếu API Keys",
                "api_keys.txt trống hoặc không tồn tại.\n"
                "Hãy nhập API key vào panel bên trái và bấm Save.",
            )
            return

        if self.is_running:
            messagebox.showinfo("Đang chạy", "Đợi tiến trình hiện tại kết thúc.")
            return

        self.is_running = True
        self.api_error_shown = False
        self.log("===== 🚀 RUN FULL PIPELINE B2→B6 =====")
        self.set_status("Đang chạy pipeline B2→B6...", ok=None)

        steps = [
            ("generate_chapters_from_idea.py", "B2 – Chapters"),
            ("generate_scenes_from_chapters.py", "B3 – Scenes"),
            ("generate_prompts.py", "B4 – Prompts"),
            ("postprocess_output_prompts.py", "B5 – Postprocess"),
            ("translate_prompts.py", "B6 – Translate"),
        ]

        def worker():
            try:
                for script, label in steps:
                    self.log(f"\n▶ {label} ({script}) ...")
                    self.set_status(f"Đang chạy {label}", ok=None)

                    proc = subprocess.Popen(
                        [sys.executable, str(BASE_DIR / script)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        cwd=str(BASE_DIR),
                    )
                    assert proc.stdout is not None

                    for line in proc.stdout:
                        line = line.rstrip("\n")
                        if not line:
                            continue

                        if "API key expired" in line or "API_KEY_INVALID" in line:
                            if not self.api_error_shown:
                                messagebox.showerror(
                                    "API Key Error",
                                    "API key bị lỗi hoặc hết hạn. Hãy kiểm tra lại api_keys.txt.",
                                )
                                self.api_error_shown = True

                        self.log(line)

                    code = proc.wait()
                    if code != 0:
                        self.log(f"❌ {label} lỗi (exit code {code}). Pipeline dừng.")
                        self.set_status(f"Lỗi ở {label}", ok=False)
                        return

                self.log(
                    "\n🎉 Pipeline B2→B6 HOÀN TẤT! Bạn có thể mở final_prompts_en.txt / final_prompts_vi.txt."
                )
                self.set_status("Pipeline hoàn tất", ok=True)

            finally:
                self.is_running = False

        threading.Thread(target=worker, daemon=True).start()

    # ===========================
    # SUPPORT FUNCS
    # ===========================
    def save_api(self):
        text = self.api_text.get("1.0", tk.END).strip()
        API_KEYS_FILE.write_text(text, encoding="utf-8")
        self.log("💾 Đã lưu API Keys vào api_keys.txt.")
        self.set_status("API Keys saved", ok=True)

    def load_api_keys(self):
        if API_KEYS_FILE.exists():
            self.api_text.delete("1.0", tk.END)
            self.api_text.insert("1.0", API_KEYS_FILE.read_text(encoding="utf-8"))

    def log(self, msg: str):
        self.log_box.insert(tk.END, msg + "\n")
        self.log_box.see(tk.END)

    def clear_log(self):
        self.log_box.delete("1.0", tk.END)

    def set_status(self, text: str, ok=True):
        if ok is True:
            color = "lightgreen"
        elif ok is False:
            color = "tomato"
        else:
            color = "yellow"
        self.status_label.config(text=text, foreground=color)

    def on_close(self):
        self.root.destroy()


# ===========================
# MAIN
# ===========================
def main():
    root = tk.Tk()
    app = FilmAIGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
