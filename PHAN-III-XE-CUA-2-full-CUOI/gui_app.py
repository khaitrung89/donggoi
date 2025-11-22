import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import subprocess
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Mapping bước -> file txt chính
STEP_FILES = {
    "B0": "story_seed.txt",
    "B1": "story_idea.txt",
    "B2": "story_lock_in.txt",      # ✅ dùng lock_in, KHÔNG còn blueprint
    "B3": "chapters_editable.txt",
    "B4": "scenes.txt",
    "B5": "output_prompts.txt",
    "B6": "output_prompts_clean.txt",
    "B7": "final_prompts_en.txt",   # mặc định hiển thị EN, có nút chuyển EN/VI
}

# Mapping bước -> script cần chạy
STEP_SCRIPTS = {
    "B1": ["generate_story_idea_from_seed.py"],
    "B2": ["generate_story_lock_in.py"],
    "B3": ["generate_chapters.py"],
    "B4": ["generate_scenes_from_chapters.py"],
    "B5": ["generate_prompts.py"],
    "B6": ["postprocess_output_prompts.py"],    # Clean
    # B7 sẽ gọi translate_prompts.py khi bấm Export Final
}


class StoryPipelineGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Siêu Prompt Tool – Story Pipeline B0 → B7 (No License)")
        self.root.geometry("1280x720")

        self.current_step = "B0"
        self.current_lang = "EN"  # cho B7 view

        self._build_layout()
        self.load_step("B0")

    # ================= LAYOUT CHÍNH =================
    def _build_layout(self):
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        # Sidebar trái
        sidebar = tk.Frame(self.root, bg="#111417", width=180)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)

        tk.Label(
            sidebar,
            text="Siêu Prompt Tool\nPipeline B0 → B7",
            fg="#00e0ff", bg="#111417",
            font=("Segoe UI", 11, "bold"),
            justify="left"
        ).pack(pady=(10, 10), anchor="w", padx=10)

        # Nút bước
        self.step_buttons = {}
        for code, label in [
            ("B0", "B0 – Seed"),
            ("B1", "B1 – Idea"),
            ("B2", "B2 – Lock-In"),
            ("B3", "B3 – Chapters"),
            ("B4", "B4 – Scenes"),
            ("B5", "B5 – Prompts"),
            ("B6", "B6 – Clean"),
            ("B7", "B7 – Final"),
        ]:
            btn = tk.Button(
                sidebar,
                text=label,
                width=18,
                relief="flat",
                bg="#1c2228",
                fg="#ffffff",
                activebackground="#00a2ff",
                activeforeground="#ffffff",
                command=lambda c=code: self.load_step(c)
            )
            btn.pack(pady=3, padx=8, anchor="w")
            self.step_buttons[code] = btn

        # Nút mở thư mục
        tk.Button(
            sidebar,
            text="📂 Mở thư mục dự án",
            relief="flat",
            bg="#222830",
            fg="#ffffff",
            command=self.open_project_folder
        ).pack(side="bottom", pady=10, padx=8, anchor="w")

        # Khu vực main editor + log
        main_frame = tk.Frame(self.root, bg="#0d1117")
        main_frame.grid(row=0, column=1, sticky="nsew")
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=0)
        main_frame.columnconfigure(0, weight=1)

        # Thanh info top
        top_bar = tk.Frame(main_frame, bg="#161b22")
        top_bar.grid(row=0, column=0, sticky="ew")

        self.mode_label = tk.Label(
            top_bar,
            text="Mode: DEV | Step: B0",
            bg="#161b22",
            fg="#58a6ff",
            font=("Segoe UI", 10, "bold")
        )
        self.mode_label.pack(side="left", padx=10, pady=4)

        self.step_desc_label = tk.Label(
            top_bar,
            text="B0 – Story Seed (Ý tưởng gốc + GENRE + STYLE).",
            bg="#161b22",
            fg="#8b949e",
            font=("Segoe UI", 9)
        )
        self.step_desc_label.pack(side="left", padx=10)

        # B7 view toggle
        self.b7_view_frame = tk.Frame(top_bar, bg="#161b22")
        self.b7_view_frame.pack(side="right", padx=10)
        tk.Label(
            self.b7_view_frame,
            text="B7 View:",
            bg="#161b22",
            fg="#8b949e",
            font=("Segoe UI", 9)
        ).pack(side="left")
        self.btn_b7_en = tk.Button(
            self.b7_view_frame,
            text="EN",
            width=3,
            relief="sunken",
            bg="#238636",
            fg="#ffffff",
            command=lambda: self.switch_b7_lang("EN")
        )
        self.btn_b7_en.pack(side="left", padx=2)
        self.btn_b7_vi = tk.Button(
            self.b7_view_frame,
            text="VI",
            width=3,
            relief="flat",
            bg="#30363d",
            fg="#ffffff",
            command=lambda: self.switch_b7_lang("VI")
        )
        self.btn_b7_vi.pack(side="left", padx=2)

        # Editor
        editor_frame = tk.Frame(main_frame, bg="#0d1117")
        editor_frame.grid(row=0, column=0, sticky="nsew")
        editor_frame.rowconfigure(0, weight=1)
        editor_frame.columnconfigure(0, weight=1)

        self.text_editor = scrolledtext.ScrolledText(
            editor_frame,
            wrap="word",
            bg="#0d1117",
            fg="#e6edf3",
            insertbackground="#e6edf3",
            font=("Consolas", 10),
        )
        self.text_editor.grid(row=0, column=0, sticky="nsew")

        # Log
        log_frame = tk.Frame(main_frame, bg="#111417", height=120)
        log_frame.grid(row=1, column=0, sticky="ew")
        log_frame.grid_propagate(False)
        log_frame.columnconfigure(0, weight=1)

        tk.Label(
            log_frame,
            text="Tiến trình / Log:",
            bg="#111417",
            fg="#8b949e",
            font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(4, 0))

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap="word",
            height=6,
            bg="#0d1117",
            fg="#9ca3af",
            insertbackground="#e6edf3",
            font=("Consolas", 9),
        )
        self.log_text.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)

        # Bottom buttons
        bottom_bar = tk.Frame(self.root, bg="#161b22", height=40)
        bottom_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        bottom_bar.grid_propagate(False)

        self.btn_b0_form = tk.Button(
            bottom_bar,
            text="📝 B0 Form",
            bg="#30363d",
            fg="#ffffff",
            relief="flat",
            command=self.open_b0_form
        )
        self.btn_b0_form.pack(side="left", padx=8, pady=5)

        self.btn_save = tk.Button(
            bottom_bar,
            text="💾 Save",
            bg="#238636",
            fg="#ffffff",
            relief="flat",
            command=self.save_current_step
        )
        self.btn_save.pack(side="left", padx=8, pady=5)

        self.btn_run_next = tk.Button(
            bottom_bar,
            text="▶ Run Next Step",
            bg="#1f6feb",
            fg="#ffffff",
            relief="flat",
            command=self.run_next_step
        )
        self.btn_run_next.pack(side="left", padx=8, pady=5)

        self.btn_export_final = tk.Button(
            bottom_bar,
            text="⬇ Export Final",
            bg="#8957e5",
            fg="#ffffff",
            relief="flat",
            command=self.export_final
        )
        self.btn_export_final.pack(side="right", padx=8, pady=5)

        self.btn_clear_log = tk.Button(
            bottom_bar,
            text="🧹 Clear log",
            bg="#30363d",
            fg="#ffffff",
            relief="flat",
            command=lambda: self.log_text.delete("1.0", tk.END)
        )
        self.btn_clear_log.pack(side="right", padx=8, pady=5)

    # ================== STEP HANDLING ==================
    def set_step_ui(self, step: str):
        # highlight nút step
        for code, btn in self.step_buttons.items():
            if code == step:
                btn.configure(bg="#00a2ff")
            else:
                btn.configure(bg="#1c2228")

        self.mode_label.config(text=f"Mode: DEV | Step: {step}")

        desc_map = {
            "B0": "B0 – Story Seed: Ý tưởng gốc + GENRE + STYLE.",
            "B1": "B1 – Story IDEA: Khung thế giới & nhân vật (BLUEPRINT mềm).",
            "B2": "B2 – Story Lock-In: Bản khóa cấu trúc cốt truyện (core spine).",
            "B3": "B3 – Chapters: Sinh từng tập theo công thức 6 phần + 3 quy tắc vàng.",
            "B4": "B4 – Scenes: Sinh SCENES chi tiết từ chapters.",
            "B5": "B5 – Prompts: Sinh PROMPT từ scenes.",
            "B6": "B6 – Clean: Làm sạch JSON / text.",
            "B7": "B7 – Final: Xem & xuất EN / VI.",
        }
        self.step_desc_label.config(text=desc_map.get(step, ""))

        # B7 view toggle
        if step == "B7":
            self.b7_view_frame.pack(side="right", padx=10)
        else:
            self.b7_view_frame.pack_forget()

    def load_step(self, step: str):
        self.current_step = step
        self.set_step_ui(step)
        self.text_editor.delete("1.0", tk.END)

        file_name = STEP_FILES.get(step)
        if not file_name:
            return

        file_path = BASE_DIR / file_name
        if file_path.exists():
            try:
                content = file_path.read_text(encoding="utf-8")
                self.text_editor.insert("1.0", content)
                self.log(f"📄 Đã mở {file_name}.")
            except Exception as e:
                self.log(f"❌ Lỗi đọc {file_name}: {e}")
        else:
            placeholder = self.get_placeholder_for_step(step)
            if placeholder:
                self.text_editor.insert("1.0", placeholder)
                self.log(f"ℹ {file_name} chưa tồn tại. Đang hiển thị template mẫu cho {step}.")
            else:
                self.log(f"ℹ {file_name} chưa tồn tại.")

    def get_placeholder_for_step(self, step: str) -> str:
        if step == "B0":
            return (
                "STORY_IDEA:\n"
                "[Viết ý tưởng tự do ở đây, 3–10 câu, < 500 từ]\n\n"
                "GENRES:\n"
                "[Ví dụ: Monster Fantasy, Adventure, Drama]\n\n"
                "STYLE_FORMAT:\n"
                "[Ví dụ: Cinematic realistic, 3D CGI, Series 10 tập, tone u tối nhưng cảm động]\n\n"
                "WORLD_ERA:\n"
                "[Ví dụ: Thế giới fantasy cổ đại, phong cách Tây Vực – Ba Tư]\n\n"
                "TONE:\n"
                "[Ví dụ: Epic, emotional, dark but hopeful]\n\n"
                "EPISODES:\n"
                "[Ví dụ: 12]\n\n"
                "SCENES_PER_EPISODE:\n"
                "[Ví dụ: 15]\n"
            )
        return ""

    def save_current_step(self):
        step = self.current_step
        file_name = STEP_FILES.get(step)
        if not file_name:
            messagebox.showinfo("Thông báo", "Bước này không có file để lưu.")
            return

        file_path = BASE_DIR / file_name
        try:
            content = self.text_editor.get("1.0", tk.END)
            file_path.write_text(content, encoding="utf-8")
            self.log(f"💾 Đã lưu {file_name}.")
        except Exception as e:
            self.log(f"❌ Lỗi khi lưu {file_name}: {e}")
            messagebox.showerror("Lỗi", f"Không lưu được {file_name}:\n{e}")

    # ================== B0 FORM ==================
    def open_b0_form(self):
        """Popup form thuận tiện để nhập Seed (B0)"""
        form = tk.Toplevel(self.root)
        form.title("B0 – Nhập Ý TƯỞNG GỐC + GENRE + STYLE")
        form.geometry("700x600")
        form.transient(self.root)
        form.grab_set()

        # Scrollable frame
        canvas = tk.Canvas(form, bg="#0d1117")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(form, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        inner = tk.Frame(canvas, bg="#0d1117")
        canvas.create_window((0, 0), window=inner, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner.bind("<Configure>", on_configure)

        # STORY IDEA
        tk.Label(inner, text="STORY_IDEA (3–10 câu):", fg="#58a6ff", bg="#0d1117",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 2))
        txt_story = scrolledtext.ScrolledText(
            inner, wrap="word", height=6,
            bg="#0d1117", fg="#e6edf3", insertbackground="#e6edf3", font=("Consolas", 10)
        )
        txt_story.pack(fill="both", expand=False, padx=10)

        # GENRES
        tk.Label(inner, text="GENRES (gõ hoặc chọn, có thể nhiều):", fg="#3fb950", bg="#0d1117",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 2))
        txt_genres = scrolledtext.ScrolledText(
            inner, wrap="word", height=4,
            bg="#0d1117", fg="#e6edf3", insertbackground="#e6edf3", font=("Consolas", 10)
        )
        txt_genres.insert("1.0", "Monster Fantasy, Adventure, Drama")
        txt_genres.pack(fill="both", expand=False, padx=10)

        # STYLE_FORMAT
        tk.Label(inner, text="STYLE_FORMAT (Phong cách phim):", fg="#f0883e", bg="#0d1117",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 2))
        txt_style = scrolledtext.ScrolledText(
            inner, wrap="word", height=3,
            bg="#0d1117", fg="#e6edf3", insertbackground="#e6edf3", font=("Consolas", 10)
        )
        txt_style.insert(
            "1.0",
            "Cinematic realistic, 3D CGI, Series 10 tập, tone u tối nhưng cảm động"
        )
        txt_style.pack(fill="both", expand=False, padx=10)

        # WORLD_ERA
        tk.Label(inner, text="WORLD_ERA (Thế giới & thời đại):", fg="#58a6ff", bg="#0d1117",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 2))
        txt_world = scrolledtext.ScrolledText(
            inner, wrap="word", height=3,
            bg="#0d1117", fg="#e6edf3", insertbackground="#e6edf3", font=("Consolas", 10)
        )
        txt_world.insert(
            "1.0",
            "Thế giới fantasy cổ đại kiểu Tây Vực – Ba Tư, ma thuật & quái thú tồn tại thật."
        )
        txt_world.pack(fill="both", expand=False, padx=10)

        # TONE
        tk.Label(inner, text="TONE (Không khí cảm xúc chính):", fg="#f0883e", bg="#0d1117",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 2))
        txt_tone = scrolledtext.ScrolledText(
            inner, wrap="word", height=2,
            bg="#0d1117", fg="#e6edf3", insertbackground="#e6edf3", font=("Consolas", 10)
        )
        txt_tone.insert("1.0", "Epic, emotional, dark but hopeful")
        txt_tone.pack(fill="both", expand=False, padx=10)

        # EPISODES + SCENES
        bottom_form = tk.Frame(inner, bg="#0d1117")
        bottom_form.pack(fill="x", padx=10, pady=(10, 10))

        tk.Label(bottom_form, text="EPISODES:", bg="#0d1117", fg="#8b949e").grid(row=0, column=0, sticky="w")
        ent_eps = tk.Entry(bottom_form, width=8, bg="#0d1117", fg="#e6edf3", insertbackground="#e6edf3")
        ent_eps.insert(0, "12")
        ent_eps.grid(row=0, column=1, sticky="w", padx=(4, 20))

        tk.Label(bottom_form, text="SCENES_PER_EPISODE:", bg="#0d1117", fg="#8b949e").grid(row=0, column=2, sticky="w")
        ent_scenes = tk.Entry(bottom_form, width=8, bg="#0d1117", fg="#e6edf3", insertbackground="#e6edf3")
        ent_scenes.insert(0, "15")
        ent_scenes.grid(row=0, column=3, sticky="w", padx=(4, 0))

        def save_b0_from_form():
            seed_lines = []
            seed_lines.append("STORY_IDEA:\n" + txt_story.get("1.0", tk.END).strip() + "\n")
            seed_lines.append("GENRES:\n" + txt_genres.get("1.0", tk.END).strip() + "\n")
            seed_lines.append("STYLE_FORMAT:\n" + txt_style.get("1.0", tk.END).strip() + "\n")
            seed_lines.append("WORLD_ERA:\n" + txt_world.get("1.0", tk.END).strip() + "\n")
            seed_lines.append("TONE:\n" + txt_tone.get("1.0", tk.END).strip() + "\n")
            seed_lines.append("EPISODES:\n" + ent_eps.get().strip() + "\n")
            seed_lines.append("SCENES_PER_EPISODE:\n" + ent_scenes.get().strip() + "\n")

            seed_text = "\n".join(seed_lines)

            file_path = BASE_DIR / STEP_FILES["B0"]
            file_path.write_text(seed_text, encoding="utf-8")
            self.log("💾 Đã lưu story_seed.txt từ B0 Form.")
            # đồng bộ editor chính
            if self.current_step == "B0":
                self.text_editor.delete("1.0", tk.END)
                self.text_editor.insert("1.0", seed_text)
            form.destroy()

        tk.Button(
            bottom_form,
            text="💾 Lưu B0 → story_seed.txt",
            bg="#238636",
            fg="#ffffff",
            relief="flat",
            command=save_b0_from_form
        ).grid(row=1, column=0, columnspan=4, pady=(10, 0), sticky="w")

    # ================== RUN NEXT STEP ==================
    def run_next_step(self):
        order = ["B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"]
        if self.current_step not in order:
            return
        idx = order.index(self.current_step)
        if idx >= len(order) - 1:
            self.log("✅ Đã ở bước cuối cùng (B7).")
            return

        next_step = order[idx + 1]

        # Trước khi chạy script, luôn save nội dung bước hiện tại
        self.save_current_step()

        # Nếu bước tiếp theo có script thì chạy
        scripts = STEP_SCRIPTS.get(next_step)
        if scripts:
            for script in scripts:
                self.run_script(script)

        # B7: load file final
        self.load_step(next_step)

    def run_script(self, script_name: str):
        script_path = BASE_DIR / script_name
        if not script_path.exists():
            self.log(f"⚠ Không tìm thấy script {script_name}. Bỏ qua bước này.")
            return

        self.log(f"▶ Đang chạy {script_name} ...")
        try:
            # Dùng subprocess.safe (bytes) + decode(errors='replace') để tránh UnicodeDecodeError
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(BASE_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Decode an toàn
            stdout_text = result.stdout.decode("utf-8", errors="replace") if result.stdout else ""
            stderr_text = result.stderr.decode("utf-8", errors="replace") if result.stderr else ""

            if stdout_text:
                for line in stdout_text.splitlines():
                    self.log("   " + line)
            if stderr_text:
                self.log("⚠ STDERR:")
                for line in stderr_text.splitlines():
                    self.log("   " + line)

            if result.returncode == 0:
                self.log(f"✅ {script_name} chạy xong.")
            else:
                self.log(f"❌ {script_name} lỗi, mã trả về {result.returncode}.")
        except Exception as e:
            self.log(f"❌ Lỗi khi chạy {script_name}: {e}")

    # ================== B7 & EXPORT ==================
    def switch_b7_lang(self, lang: str):
        self.current_lang = lang
        if lang == "EN":
            self.btn_b7_en.configure(bg="#238636", relief="sunken")
            self.btn_b7_vi.configure(bg="#30363d", relief="flat")
        else:
            self.btn_b7_vi.configure(bg="#238636", relief="sunken")
            self.btn_b7_en.configure(bg="#30363d", relief="flat")

        # Nếu đang ở B7 thì load lại file tương ứng
        if self.current_step == "B7":
            if lang == "EN":
                STEP_FILES["B7"] = "final_prompts_en.txt"
            else:
                STEP_FILES["B7"] = "final_prompts_vi.txt"
            self.load_step("B7")

    def export_final(self):
        """
        B7 – Export Final:
        - Chạy translate_prompts.py để tạo final_prompts_en.txt + final_prompts_vi.txt
        - Cho user chọn thư mục để copy kết quả ra ngoài (optional)
        """
        # luôn cố chạy translate_prompts trước khi export
        script = BASE_DIR / "translate_prompts.py"
        if script.exists():
            self.run_script("translate_prompts.py")
        else:
            self.log("⚠ Không tìm thấy translate_prompts.py, chỉ export các file hiện có.")

        # Hỏi thư mục export
        target_dir = filedialog.askdirectory(
            title="Chọn thư mục để export kết quả (Final Prompts + Story Files)"
        )
        if not target_dir:
            return

        target_dir = Path(target_dir)

        files_to_copy = [
            "story_seed.txt",
            "story_idea.txt",
            "story_lock_in.txt",
            "chapters_editable.txt",
            "scenes.txt",
            "output_prompts.txt",
            "output_prompts_clean.txt",
            "final_prompts_en.txt",
            "final_prompts_vi.txt",
        ]

        ok_count = 0
        for name in files_to_copy:
            src = BASE_DIR / name
            if src.exists():
                try:
                    dst = target_dir / name
                    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
                    ok_count += 1
                except Exception as e:
                    self.log(f"❌ Lỗi copy {name}: {e}")
            else:
                self.log(f"⚠ File {name} chưa tồn tại, bỏ qua.")

        messagebox.showinfo(
            "Export xong",
            f"Đã export {ok_count} file sang thư mục:\n{target_dir}"
        )
        self.log(f"⬇ Đã export {ok_count} file sang {target_dir}")

    # ================== UTIL ==================
    def log(self, message: str):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def open_project_folder(self):
        path = str(BASE_DIR)
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])


def main():
    root = tk.Tk()
    app = StoryPipelineGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
