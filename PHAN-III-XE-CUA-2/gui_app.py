import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import sys
import os
from pathlib import Path
import subprocess

# Import các module chính của tool
from license_manager import check_license, request_license

class PromptGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FilmAI Prompt Generator - Premium Tool")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Cấu hình style
        self.setup_styles()
        
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
        main_frame.rowconfigure(3, weight=1)
        
        # Tiêu đề
        title_label = tk.Label(main_frame, text="🎬 FilmAI Prompt Generator",
                              font=("Arial", 20, "bold"), fg=self.primary_color)
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame chọn file
        file_frame = ttk.LabelFrame(main_frame, text="Chọn file input", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        file_frame.columnconfigure(1, weight=1)
        
        # Entry đường dẫn file
        file_entry = ttk.Entry(file_frame, textvariable=self.input_file, width=60)
        file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10))
        
        # Nút chọn file
        browse_button = ttk.Button(file_frame, text="📁 Chọn file",
                                  command=self.browse_file)
        browse_button.grid(row=0, column=2, padx=(0, 10))
        
        # Mặc định chọn file scenes.txt nếu tồn tại
        default_file = Path("scenes.txt")
        if default_file.exists():
            self.input_file.set(str(default_file.absolute()))
        
        # Frame nút điều khiển
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=3, pady=(0, 15))
        
        # Nút start
        self.start_button = ttk.Button(control_frame, text="🚀 Bắt đầu chạy",
                                      command=self.start_generation,
                                      style="Accent.TButton")
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Nút dừng
        self.stop_button = ttk.Button(control_frame, text="⏹️ Dừng",
                                     command=self.stop_generation,
                                     state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Nút xem kết quả
        self.view_result_button = ttk.Button(control_frame, text="📄 Xem kết quả",
                                           command=self.view_result,
                                           state=tk.DISABLED)
        self.view_result_button.pack(side=tk.LEFT)
        
        # Frame hiển thị log
        log_frame = ttk.LabelFrame(main_frame, text="Tiến trình chạy", padding="10")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Text area cho log
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80,
                                                 font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Thanh trạng thái
        self.status_label = ttk.Label(main_frame, text="Sẵn sàng",
                                     font=("Arial", 10, "italic"))
        self.status_label.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Nút thoát
        exit_button = ttk.Button(main_frame, text="❌ Thoát",
                                command=self.on_closing)
        exit_button.grid(row=5, column=2, sticky=(tk.E), pady=(10, 0))
        
        # Bind sự kiện đóng cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def browse_file(self):
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
        
        if not input_file:
            self.log_message("❌ Vui lòng chọn file input!")
            return
            
        if not Path(input_file).exists():
            self.log_message(f"❌ File không tồn tại: {input_file}")
            return
        
        # Đổi tên file scenes.txt tạm thời để tool đọc
        original_scenes = Path("scenes.txt")
        backup_name = Path("scenes_backup.txt")
        
        try:
            # Backup file gốc nếu có
            if original_scenes.exists():
                original_scenes.rename(backup_name)
            
            # Copy file được chọn thành scenes.txt
            Path(input_file).rename(original_scenes)
            
        except Exception as e:
            self.log_message(f"❌ Lỗi khi chuẩn bị file: {e}")
            return
        
        # Cập nhật giao diện
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.view_result_button.config(state=tk.DISABLED)
        
        self.log_message("🚀 Bắt đầu generate prompts...")
        self.update_status("Đang chạy...")
        
        # Chạy tool trong thread riêng
        thread = threading.Thread(target=self.run_tool)
        thread.daemon = True
        thread.start()
        
    def run_tool(self):
        """Chạy tool generate prompts"""
        try:
            # Import và chạy tool chính
            import generate_prompts
            
            # Redirect output để hiển thị trong GUI
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            
            class StdoutRedirector:
                def __init__(self, text_widget):
                    self.text_widget = text_widget
                    
                def write(self, string):
                    if string.strip():
                        self.text_widget.insert(tk.END, string + "\n")
                        self.text_widget.see(tk.END)
                        
                def flush(self):
                    pass
            
            sys.stdout = StdoutRedirector(self.log_text)
            sys.stderr = StdoutRedirector(self.log_text)
            
            # Chạy tool
            generate_prompts.main()
            
            # Khôi phục stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
            self.log_message("✅ Hoàn thành!")
            self.update_status("Hoàn thành")
            
        except Exception as e:
            self.log_message(f"❌ Lỗi khi chạy tool: {e}")
            self.update_status("Lỗi")
            
        finally:
            # Khôi phục file gốc
            self.restore_files()
            
            # Cập nhật giao diện
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.view_result_button.config(state=tk.NORMAL)
            
    def restore_files(self):
        """Khôi phục lại các file gốc"""
        try:
            original_scenes = Path("scenes.txt")
            backup_name = Path("scenes_backup.txt")
            
            # Xóa file hiện tại
            if original_scenes.exists():
                original_scenes.unlink()
            
            # Khôi phục file backup
            if backup_name.exists():
                backup_name.rename(original_scenes)
                
        except Exception as e:
            self.log_message(f"⚠️ Cảnh báo: Không thể khôi phục file gốc: {e}")
            
    def stop_generation(self):
        """Dừng quá trình generate"""
        if self.is_running:
            self.log_message("⏹️ Đang dừng...")
            self.update_status("Đang dừng...")
            
            # Có thể thêm logic dừng ở đây nếu cần
            self.is_running = False
            
    def view_result(self):
        """Xem kết quả"""
        output_file = Path("output_prompts.txt")
        if output_file.exists():
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(output_file)
                else:  # Mac/Linux
                    subprocess.call(['open', output_file])
            except Exception as e:
                self.log_message(f"❌ Không thể mở file: {e}")
        else:
            self.log_message("❌ Không tìm thấy file kết quả: output_prompts.txt")
            
    def on_closing(self):
        """Xử lý khi đóng cửa sổ"""
        if self.is_running:
            if messagebox.askokcancel("Xác nhận", "Tool đang chạy. Bạn có chắc muốn thoát?"):
                self.restore_files()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    """Hàm chính để chạy GUI"""
    root = tk.Tk()
    app = PromptGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()