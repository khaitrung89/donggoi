import os
import sys
from pathlib import Path
import importlib
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# =========================
# CẤU HÌNH CƠ BẢN
# =========================

BASE_DIR = Path(__file__).resolve().parent

# Mapping từng bước -> file chính nó dùng
STEP_FILES = {
    "B0": [BASE_DIR / "story_seed.txt"],
    "B1": [BASE_DIR / "story_idea.txt"],
    "B2": [BASE_DIR / "story_lock_in.txt"],
    "B3": [BASE_DIR / "chapters_editable.txt"],
    "B4": [BASE_DIR / "scenes.txt"],
    "B5": [BASE_DIR / "output_prompts.txt"],
    "B6": [BASE_DIR / "output_prompts_clean.txt"],
    "B7_EN": [BASE_DIR / "final_prompts_en.txt"],
    "B7_VI": [BASE_DIR / "final_prompts_vi.txt"],
}

# Mapping bước -> module .py cần chạy cho NEXT ACTION
STEP_ACTIONS = {
    "B0": ("generate_story_idea_from_seed", "main"),         # B0 -> B1
    "B1": ("generate_story_lock_in", "main"),                # B1 -> B2
    "B2": ("generate_chapters_from_idea", "main"),           # B2 -> B3 (FIXED)
    "B3": ("generate_scenes_from_chapters", "main"),         # B3 -> B4
    "B4": ("generate_prompts", "main"),                      # B4 -> B5
    "B5": ("postprocess_output_prompts", "main"),            # B5 -> B6
    "B6": ("translate_prompts", "main"),                     # B6 -> B7
    # B7 không có step NEXT (chỉ export / refresh)
}

# Text hiển thị mô tả cho từng bước
STEP_DESCRIPTIONS = {
    "B0": "B0 – Story Seed: Nhập Ý TƯỞNG + GENRE + STYLE.\n"
          "→ Lưu vào story_seed.txt, sau đó sinh STORY IDEA (B1).",
    "B1": "B1 – Story Idea: Khung cốt truyện đầy đủ (tiêu đề, logline, world, nhân vật, 3 hồi...).\n"
          "→ Bạn có thể chỉnh sửa, sau đó sinh STORY LOCK-IN (B2).",
    "B2": "B2 – Story Lock-In: Bản khóa cốt truyện (core story, season arc, theme, engine...).\n"
          "→ Dùng để sinh CHAPTERS (B3).",
    "B3": "B3 – Chapters: Mỗi tập theo cấu trúc 6 phần + 3 quy tắc vàng + message + scene count.\n"
          "→ Bạn chỉnh MISSION / TWIST / MESSAGE / SCENE COUNT rồi sinh SCENES (B4).",
    "B4": "B4 – Scenes: Danh sách cảnh (CHx-Sy: mô tả thô) dùng để sinh PROMPTS (B5).",
    "B5": "B5 – Raw Prompts: Mỗi dòng là prompt chưa xử lý JSON.\n"
          "→ Chạy postprocess để chuẩn hóa (B6).",
    "B6": "B6 – Clean Prompts: Prompt tiếng Anh đã chuẩn JSON.\n"
          "→ Dịch sang EN & VI (B7).",
    "B7": "B7 – Final Prompts: final_prompts_en.txt & final_prompts_vi.txt.\n"
          "→ Dùng cho AI video / image.",
}

# =========================
# HÀM TIỆN ÍCH
# =========================

def safe_read_text(path: Path) -> str:
    try:
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""
    except Exception as e:
        return f"❌ Lỗi đọc file {path.name}: {e}"

def safe_write_text(path: Path, content: str):
    try:
        path.write_text(content, encoding="utf-8")
        return True, None
    except Exception as e:
        return False, str(e)

def run_module_action(module_name: str, func_name: str = "main"):
    """
    Import module động và gọi hàm main().
    """
    try:
        mod = importlib.import_module(module_name)
    except ImportError as e:
        messagebox.showerror("Lỗi import module", f"Không import được module '{module_name}':\n{e}")
        return False

    func = getattr(mod, func_name, None)
    if not callable(func):
        messagebox.showerror("Lỗi", f"Module '{module_name}' không có hàm '{func_name}'.")
        return False

    try:
        func()
        return True
    except Exception as e:
        messagebox.showerror("Lỗi khi chạy", f"Lỗi khi chạy {module_name}.{func_name}():\n{e}")
        return False

# =========================
# LỚP ỨNG DỤNG CHÍNH
# =========================

class SuperPromptGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Siêu Prompt Tool – Story Pipeline B0 → B7 (No License)")
        self.geometry("1200x700")

        # Chế độ: DEV / STUDIO (3 = bạn chọn)
        self.mode = tk.StringVar(value="DEV")  # DEV hoặc STUDIO

        # Bước hiện tại
        self.current_step = "B0"
        # Riêng B7 có 2 chế độ xem: EN / VI
        self.b7_lang = tk.StringVar(value="EN")

        # Flag để track trạng thái chạy pipeline
        self.is_running = False

        # Thiết lập theme đơn giản kiểu dark
        self._setup_theme()

        # Layout chính
        self._build_layout()

        # Load nội dung ban đầu
        self.load_step_content()

    # ------------- THEME ------------- #
    def _setup_theme(self):
        self.configure(bg="#1e1e1e")
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("Sidebar.TFrame", background="#252526")
        style.configure("Main.TFrame", background="#1e1e1e")
        style.configure("Step.TButton", background="#333333", foreground="#ffffff")
        style.map("Step.TButton",
                  background=[("active", "#444444")])
        style.configure("Mode.TCheckbutton", background="#252526", foreground="#ffffff")
        style.configure("Info.TLabel", background="#1e1e1e", foreground="#ffffff")

    # ------------- UI ------------- #
    def _build_layout(self):
        # Chia thành 2 cột: sidebar trái, nội dung phải
        sidebar = ttk.Frame(self, style="Sidebar.TFrame", width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        main = ttk.Frame(self, style="Main.TFrame")
        main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Sidebar: tiêu đề
        title_label = ttk.Label(
            sidebar,
            text="Siêu Prompt Tool\nPipeline B0 → B7",
            style="Info.TLabel",
            justify="center"
        )
        title_label.pack(padx=10, pady=10)

        # Sidebar: Mode switch
        mode_frame = ttk.Frame(sidebar, style="Sidebar.TFrame")
        mode_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        ttk.Label(mode_frame, text="Mode:", style="Info.TLabel").pack(side=tk.LEFT)

        mode_dev = ttk.Radiobutton(
            mode_frame, text="DEV", variable=self.mode, value="DEV",
            style="Mode.TRadiobutton"
        )
        mode_studio = ttk.Radiobutton(
            mode_frame, text="STUDIO", variable=self.mode, value="STUDIO",
            style="Mode.TRadiobutton"
        )

        # Radiobutton style might not follow Mode.T..., but we mainly care about function
        mode_dev.pack(side=tk.LEFT, padx=5)
        mode_studio.pack(side=tk.LEFT, padx=5)

        # Sidebar: Step buttons
        steps_frame = ttk.Frame(sidebar, style="Sidebar.TFrame")
        steps_frame.pack(fill=tk.Y, expand=True, padx=10, pady=10)

        self.step_buttons = {}
        step_list = [
            ("B0", "B0 – Seed"),
            ("B1", "B1 – Idea"),
            ("B2", "B2 – Lock-In"),
            ("B3", "B3 – Chapters"),
            ("B4", "B4 – Scenes"),
            ("B5", "B5 – Prompts"),
            ("B6", "B6 – Clean"),
            ("B7", "B7 – Final"),
        ]
        for code, label in step_list:
            btn = ttk.Button(
                steps_frame,
                text=label,
                style="Step.TButton",
                command=lambda c=code: self.switch_step(c),
            )
            btn.pack(fill=tk.X, pady=3)
            self.step_buttons[code] = btn

        # Sidebar: Open folder button (DEV tiện)
        open_dir_btn = ttk.Button(
            sidebar,
            text="📂 Mở thư mục dự án",
            command=self.open_base_dir
        )
        open_dir_btn.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Main: info label + text + action buttons
        top_frame = ttk.Frame(main, style="Main.TFrame")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        self.info_label = ttk.Label(
            top_frame,
            text="",
            style="Info.TLabel",
            justify="left"
        )
        self.info_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Riêng B7: lựa chọn EN/VI
        b7_lang_frame = ttk.Frame(top_frame, style="Main.TFrame")
        b7_lang_frame.pack(side=tk.RIGHT)
        ttk.Label(b7_lang_frame, text="B7 View:", style="Info.TLabel").pack(side=tk.LEFT)
        ttk.Radiobutton(
            b7_lang_frame,
            text="EN",
            variable=self.b7_lang,
            value="EN",
            command=self.load_step_content
        ).pack(side=tk.LEFT)
        ttk.Radiobutton(
            b7_lang_frame,
            text="VI",
            variable=self.b7_lang,
            value="VI",
            command=self.load_step_content
        ).pack(side=tk.LEFT)

        # Main: text area với scrollbar
        text_frame = ttk.Frame(main, style="Main.TFrame")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.text_widget = tk.Text(
            text_frame,
            wrap="word",
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="#ffffff",
            font=("Consolas", 11)
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.configure(yscrollcommand=scrollbar.set)

        # Main: action buttons
        action_frame = ttk.Frame(main, style="Main.TFrame")
        action_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.btn_save = ttk.Button(action_frame, text="💾 Save", command=self.save_current_step)
        self.btn_run_next = ttk.Button(action_frame, text="▶ Run Next Step", command=self.run_next_step)
        self.btn_run_pipeline = ttk.Button(action_frame, text="🚀 Run B2→B6 (One-click)", command=self.run_full_pipeline)
        self.btn_export = ttk.Button(action_frame, text="📤 Export Final", command=self.export_final)

        self.btn_save.pack(side=tk.LEFT, padx=5)
        self.btn_run_next.pack(side=tk.LEFT, padx=5)
        self.btn_run_pipeline.pack(side=tk.LEFT, padx=5)
        self.btn_export.pack(side=tk.RIGHT, padx=5)

        # Mặc định B7 export button chỉ thực sự hữu ích ở bước B7
        self.update_action_buttons_visibility()

    # ------------- ACTIONS ------------- #
    def switch_step(self, step_code: str):
        self.current_step = step_code
        self.update_action_buttons_visibility()
        self.load_step_content()

    def update_action_buttons_visibility(self):
        """
        - B7: Run Next không còn ý nghĩa (vì pipeline kết thúc), chỉ dùng Export.
        - Các bước khác: Save + Run Next là chính.
        """
        if self.current_step == "B7":
            self.btn_run_next.configure(state=tk.DISABLED)
            self.btn_export.configure(state=tk.NORMAL)
        else:
            self.btn_run_next.configure(state=tk.NORMAL)
            # Export final chủ yếu ở B7; ở bước khác disable cho rõ logic
            self.btn_export.configure(state=tk.DISABLED)

    def get_files_for_current_step(self):
        """
        Trả về list Path tương ứng step hiện tại.
        Riêng B7 tùy vào EN/VI.
        """
        if self.current_step == "B7":
            if self.b7_lang.get() == "VI":
                return STEP_FILES.get("B7_VI", [])
            else:
                return STEP_FILES.get("B7_EN", [])
        return STEP_FILES.get(self.current_step, [])

    def load_step_content(self):
        files = self.get_files_for_current_step()
        self.text_widget.delete("1.0", tk.END)

        desc_key = "B7" if self.current_step == "B7" else self.current_step
        desc = STEP_DESCRIPTIONS.get(desc_key, "")
        mode_text = f"Mode: {self.mode.get()} | Step: {self.current_step}"
        if self.current_step == "B7":
            mode_text += f" | View: {self.b7_lang.get()}"
        self.info_label.config(text=f"{mode_text}\n{desc}")

        if not files:
            self.text_widget.insert(tk.END, f"# Không có file cho bước {self.current_step}\n")
            return

        # Chế độ STUDIO hay DEV đều load file, chỉ khác cách bạn dùng ngoài đời.
        # STUDIO: chỉnh trong GUI là chính, DEV: có thể mở file ngoài editor.
        content_parts = []
        for path in files:
            content = safe_read_text(path)
            if len(files) > 1:
                content_parts.append(f"===== {path.name} =====\n{content}\n")
            else:
                content_parts.append(content)

        final_content = "\n".join(content_parts)
        if not final_content.strip():
            # Nếu file trống và là B0, gợi ý template seed
            if self.current_step == "B0":
                final_content = (
                    "STORY_IDEA:\n"
                    "[Viết ý tưởng tự do ở đây, 3–10 câu, < 500 từ]\n\n"
                    "GENRES:\n"
                    "[Ví dụ: Monster Fantasy, Adventure, Drama]\n\n"
                    "STYLE_FORMAT:\n"
                    "[Ví dụ: Cinematic realistic, 3D CGI, Series 10 tập, tone u tối nhưng cảm động]\n"
                )
        self.text_widget.insert(tk.END, final_content)

    def save_current_step(self):
        files = self.get_files_for_current_step()
        if not files:
            messagebox.showinfo("Thông báo", "Không có file nào để lưu cho bước này.")
            return

        content = self.text_widget.get("1.0", tk.END)
        # Với B7 có 2 file, ta chỉ cho save file đang xem (EN hoặc VI).
        target = files[0]

        ok, err = safe_write_text(target, content)
        if ok:
            messagebox.showinfo("Đã lưu", f"Đã lưu nội dung vào {target.name}")
        else:
            messagebox.showerror("Lỗi lưu file", f"Không thể lưu {target.name}:\n{err}")

    def run_next_step(self):
        """
        Tùy step hiện tại, gọi module tương ứng trong STEP_ACTIONS.
        Trước khi chạy, luôn SAVE nội dung text vào file cho bước hiện tại.
        Sau khi chạy thành công, tự động chuyển sang bước kế.
        """
        # 1) Save nội dung hiện tại
        self.save_current_step()

        # 2) Xem step hiện tại có action không?
        action = STEP_ACTIONS.get(self.current_step)
        if not action:
            messagebox.showinfo("Thông báo", f"Bước {self.current_step} không có step NEXT.")
            return

        module_name, func_name = action
        ok = run_module_action(module_name, func_name)
        if not ok:
            return

        # 3) Chuyển step
        next_step = None
        if self.current_step == "B0":
            next_step = "B1"
        elif self.current_step == "B1":
            next_step = "B2"
        elif self.current_step == "B2":
            next_step = "B3"
        elif self.current_step == "B3":
            next_step = "B4"
        elif self.current_step == "B4":
            next_step = "B5"
        elif self.current_step == "B5":
            next_step = "B6"
        elif self.current_step == "B6":
            next_step = "B7"

        if next_step:
            self.switch_step(next_step)
            messagebox.showinfo("Thành công", f"Đã chạy {module_name}.{func_name}() và chuyển sang {next_step}.")
        else:
            messagebox.showinfo("Hoàn tất", "Pipeline đã đến bước cuối cùng.")

    def run_full_pipeline(self):
        """
        Chạy toàn bộ pipeline B2 → B6 một lần (One-click mode)
        Yêu cầu: story_idea.txt đã có (tức B0/B1 đã hoàn tất)
        """
        # Kiểm tra story_idea.txt
        story_idea_file = BASE_DIR / "story_idea.txt"
        if not story_idea_file.exists() or not story_idea_file.read_text(encoding="utf-8").strip():
            messagebox.showwarning(
                "Thiếu story_idea.txt",
                "Chưa có story_idea.txt hoặc file trống.\n"
                "Hãy hoàn tất B0 (Nhập ý tưởng) trước khi chạy pipeline."
            )
            return

        # Kiểm tra đang chạy
        if self.is_running:
            messagebox.showinfo("Đang chạy", "Đang có tiến trình khác đang chạy. Vui lòng đợi.")
            return

        self.is_running = True

        # Danh sách các bước cần chạy
        steps = [
            ("generate_chapters_from_idea", "main", "B2 - Generate CHAPTERS"),
            ("generate_scenes_from_chapters", "main", "B3 - Generate SCENES"),
            ("generate_prompts", "main", "B4 - Generate PROMPTS"),
            ("postprocess_output_prompts", "main", "B5 - Postprocess PROMPTS"),
            ("translate_prompts", "main", "B6 - Translate PROMPTS"),
        ]

        def worker():
            try:
                for module_name, func_name, label in steps:
                    print(f"\n▶️ ĐANG CHẠY {label} ({module_name}.{func_name})...")

                    try:
                        mod = importlib.import_module(module_name)
                        func = getattr(mod, func_name, None)
                        if not callable(func):
                            messagebox.showerror("Lỗi", f"Module '{module_name}' không có hàm '{func_name}'.")
                            return
                        func()
                        print(f"✅ {label} hoàn thành.")
                    except Exception as e:
                        messagebox.showerror("Lỗi", f"Lỗi khi chạy {label}:\n{e}")
                        return

                # Hoàn tất
                messagebox.showinfo(
                    "Hoàn tất Pipeline",
                    "🎉 Đã chạy xong toàn bộ pipeline B2→B6!\n\n"
                    "File output:\n"
                    "- output_prompts_clean.txt (MASTER EN)\n"
                    "- final_prompts_en.txt\n"
                    "- final_prompts_vi.txt"
                )

                # Tự động chuyển sang B7 để xem kết quả
                self.switch_step("B7")

            finally:
                self.is_running = False

        # Chạy trong thread riêng để không block GUI
        threading.Thread(target=worker, daemon=True).start()

    def export_final(self):
        """
        B7 – cho phép export toàn bộ file final_prompts_en.txt & final_prompts_vi.txt
        sang thư mục người dùng chọn.
        """
        target_dir = filedialog.askdirectory(
            title="Chọn thư mục để export final prompts"
        )
        if not target_dir:
            return

        target_dir = Path(target_dir)
        files_to_export = [
            ("final_prompts_en.txt", STEP_FILES.get("B7_EN", [None])[0]),
            ("final_prompts_vi.txt", STEP_FILES.get("B7_VI", [None])[0]),
        ]

        copied = []
        for name, src in files_to_export:
            if not src or not src.exists():
                continue
            dest = target_dir / name
            try:
                dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
                copied.append(str(dest))
            except Exception as e:
                messagebox.showerror("Lỗi export", f"Không thể export {name}:\n{e}")

        if copied:
            messagebox.showinfo("Export xong", "Đã export các file:\n" + "\n".join(copied))
        else:
            messagebox.showwarning("Không có file", "Không tìm thấy final_prompts_en/vi để export.")

    def open_base_dir(self):
        """
        Mở thư mục dự án (BASE_DIR) trong hệ thống.
        Hữu ích cho DEV mode.
        """
        path = str(BASE_DIR)
        if sys.platform.startswith("win"):
            os.startfile(path)  # type: ignore
        elif sys.platform == "darwin":
            os.system(f'open "{path}"')
        else:
            os.system(f'xdg-open "{path}"')


def main():
    """
    Entry point for GUI application.
    Called by main.py after license verification.
    """
    app = SuperPromptGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
