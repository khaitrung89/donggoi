# 🪟 HƯỚNG DẪN BUILD .EXE TRÊN WINDOWS

## ⚠️ LƯU Ý QUAN TRỌNG

**PyInstaller KHÔNG hỗ trợ cross-compile:**
- Build trên Windows → `.exe` cho Windows ✅
- Build trên Linux → binary cho Linux ❌
- Build trên Mac → `.app` cho Mac ❌

**Để tạo file .exe, BẮT BUỘC phải build trên máy Windows!**

---

## 📋 YÊU CẦU HỆ THỐNG

- **Windows 10/11** (64-bit khuyến nghị)
- **Python 3.8+** (khuyến nghị Python 3.11)
- **Internet connection** (để cài dependencies)
- **~500MB dung lượng trống**

---

## 🚀 HƯỚNG DẪN BUILD CHI TIẾT

### **Bước 1: Cài đặt Python**

1. Tải Python từ: https://www.python.org/downloads/
2. Chọn **Python 3.11** (khuyến nghị)
3. **QUAN TRỌNG:** Tick vào ☑️ "Add Python to PATH" khi cài đặt
4. Verify cài đặt:
```cmd
python --version
pip --version
```

### **Bước 2: Clone hoặc copy project về máy**

```cmd
# Nếu dùng git
git clone https://github.com/khaitrung89/donggoi.git
cd donggoi\PHAN-III-Chat-AI-Final-Anh-CUOI-ko-MOTA-xe-cua

# Hoặc giải nén ZIP và cd vào thư mục
```

### **Bước 3: Cài đặt dependencies**

Mở **Command Prompt** hoặc **PowerShell** trong thư mục project:

```cmd
# Cài đặt requirements
pip install -r requirements.txt

# Cài đặt PyInstaller
pip install pyinstaller
```

### **Bước 4: Chuẩn bị file config**

Đảm bảo các file sau tồn tại:
- ✅ `api_keys.txt` - Ít nhất 1 Gemini API key
- ✅ `character_dictionary.json`
- ✅ `camera_styles.txt`
- ✅ `extras_worlds.json`
- ✅ `scenes.txt` hoặc `scenes_test.txt`

### **Bước 5: Fix bug trong build.spec**

**Bug đã được fix:** File `build.spec` đã được cập nhật để dùng `SPECPATH` thay vì `__file__`

Nếu bạn gặp lỗi, đảm bảo dòng 8 trong `build.spec` là:
```python
current_dir = Path(SPECPATH).absolute()
```

### **Bước 6: Chạy build script**

```cmd
# Cách 1: Dùng build script tự động (khuyến nghị)
python build_exe.py

# Cách 2: Chạy PyInstaller trực tiếp
pyinstaller --clean --noconfirm build.spec
```

### **Bước 7: Kiểm tra kết quả**

Sau khi build thành công:

```
📁 dist/
   └── FilmAI-PromptGenerator.exe  ← File .exe chính
   └── ... (các file dependency)
```

**File size:** Khoảng 80-150MB (bình thường)

---

## ✅ TEST CHƯƠNG TRÌNH

### **Test 1: Chạy file .exe**

```cmd
cd dist
FilmAI-PromptGenerator.exe
```

**Kết quả mong đợi:**
- Hiện cửa sổ GUI
- Yêu cầu nhập license key
- Nhập một trong các key mẫu:
  - `ABCD-EFGH-IJKL-MNOP`
  - `1234-5678-9012-3456`
  - `TEST-KEYS-2024-DEMO`

### **Test 2: Generate prompts**

1. Click "Chọn file" → chọn `scenes_test.txt`
2. Click "Bắt đầu chạy"
3. Đợi xử lý (khoảng 1-2 phút cho 4 scenes)
4. Kiểm tra `output_prompts.txt` được tạo

### **Test 3: Translate prompts**

```cmd
# Chạy translate script trong thư mục gốc (không phải dist)
python translate_prompts.py
```

Kiểm tra 2 file output:
- `final_prompts_en.txt`
- `final_prompts_vi.txt`

---

## 🐛 TROUBLESHOOTING

### ❌ Lỗi: "Python không được nhận dạng..."

**Nguyên nhân:** Python chưa được thêm vào PATH

**Giải pháp:**
1. Gỡ cài Python
2. Cài lại và tick ☑️ "Add Python to PATH"
3. Restart Command Prompt

### ❌ Lỗi: "No module named 'google.generativeai'"

**Giải pháp:**
```cmd
pip install google-generativeai
```

### ❌ Lỗi: Build thành công nhưng .exe không chạy

**Kiểm tra:**
1. Antivirus có block không? → Tạm tắt
2. Windows Defender SmartScreen → Click "More info" → "Run anyway"
3. Chạy Command Prompt as Administrator:
```cmd
cd dist
FilmAI-PromptGenerator.exe
```

### ❌ Lỗi: "Failed to execute script"

**Nguyên nhân:** Thiếu dependencies hoặc data files

**Giải pháp:**
1. Kiểm tra thư mục `dist/` có các file .txt, .json không
2. Rebuild với:
```cmd
pyinstaller --clean --noconfirm build.spec
```

### ❌ File .exe quá lớn (>200MB)

**Bình thường:** 80-150MB là OK

**Nếu >200MB:** Có thể optimize bằng UPX:
```cmd
# Tải UPX: https://github.com/upx/upx/releases
# Đặt upx.exe vào PATH
# Rebuild sẽ tự động compress
```

---

## 📦 PHÂN PHỐI TOOL

### **Option 1: Phân phối thư mục dist/**

```
📁 FilmAI-PromptGenerator/
   ├── FilmAI-PromptGenerator.exe
   ├── api_keys.txt
   ├── camera_styles.txt
   ├── character_dictionary.json
   ├── extras_worlds.json
   ├── scenes.txt
   └── ... (dependency files)
```

**Hướng dẫn user:**
1. Giải nén thư mục
2. Chỉnh sửa `api_keys.txt`, `scenes.txt`
3. Chạy `FilmAI-PromptGenerator.exe`

### **Option 2: Tạo installer với Inno Setup**

1. Tải Inno Setup: https://jrsoftware.org/isdl.php
2. Tạo script cài đặt
3. Build thành file setup.exe

---

## 🔧 BUILD CHO PHÂN PHỐI RỘNG RÃI

### **Tăng cường bảo mật license:**

File `license_manager.py` hiện tại có vấn đề:
- ⚠️ Hardcode keys trong source → dễ reverse
- ⚠️ Dùng MD5 hash (yếu)
- ⚠️ Dễ bypass

**Khuyến nghị cho version commercial:**
1. Implement online license validation
2. Sử dụng license server
3. Encrypt API keys
4. Obfuscate code với PyArmor

### **Code signing (để Windows không cảnh báo)**

1. Mua Code Signing Certificate
2. Sign file .exe:
```cmd
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com FilmAI-PromptGenerator.exe
```

---

## 📊 KÍCH THƯỚC VÀ PERFORMANCE

| Metric | Value |
|--------|-------|
| Build time | 2-5 phút |
| .exe size | 80-150 MB |
| Startup time | 2-5 giây |
| Memory usage | 100-200 MB |

---

## 🎯 CHECKLIST TRƯỚC KHI PHÂN PHỐI

- [ ] Test .exe trên máy Windows sạch (không có Python)
- [ ] Test với Windows Defender bật
- [ ] Test license system hoạt động
- [ ] Kiểm tra API keys mẫu
- [ ] Viết README cho end-user
- [ ] Chuẩn bị support docs
- [ ] Test với scenes.txt thật (60+ scenes)
- [ ] Kiểm tra error handling
- [ ] Backup source code

---

## 📞 HỖ TRỢ

**Nếu gặp vấn đề:**
1. Check log output trong GUI
2. Chạy từ Command Prompt để xem error
3. Kiểm tra antivirus/firewall
4. Đảm bảo internet connection (cho Gemini API)

---

## 📝 NOTES

- Build script đã được fix bug `__file__` → `SPECPATH`
- GUI version chỉ build được trên Windows
- Linux/Mac cần build CLI version riêng
- Nên test kỹ license system trước khi distribute

**Good luck! 🚀**
