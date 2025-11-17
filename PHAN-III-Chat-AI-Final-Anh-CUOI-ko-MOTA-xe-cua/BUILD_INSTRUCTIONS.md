# FilmAI Prompt Generator - Premium Tool

## 🎬 Giới thiệu
Tool chuyên nghiệp để generate prompts cho AI hình ảnh, với giao diện GUI và hệ thống bản quyền.

## 🔐 Hệ thống bản quyền

### Key bản quyền mẫu (để test):
- `ABCD-EFGH-IJKL-MNOP`
- `1234-5678-9012-3456`
- `TEST-KEYS-2024-DEMO`
- `PROD-UCTI-ONKE-Y2024`

### Format key:
- 4 nhóm, mỗi nhóm 4 ký tự
- Cách nhau bằng dấu gạch ngang
- Ví dụ: `XXXX-XXXX-XXXX-XXXX`

## 🚀 Cách sử dụng

### 1. Chạy trực tiếp (có Python):
```bash
# Cài dependencies
pip install -r requirements.txt

# Chạy giao diện GUI
python gui_app.py

# Hoặc chạy command line
python generate_prompts.py
```

### 2. Chạy file .exe (không cần Python):
- Chạy file `dist/FilmAI-PromptGenerator.exe`
- Nhập key bản quyền khi được yêu cầu
- Sử dụng giao diện GUI để chọn file và generate

## 🏗️ Build từ source

### Cách 1: Dùng build script
```bash
python build_exe.py
```

### Cách 2: Dùng PyInstaller trực tiếp
```bash
# Cài PyInstaller
pip install pyinstaller

# Build với spec file
pyinstaller --clean --noconfirm build.spec
```

## 📁 File structure sau khi build:
```
dist/
├── FilmAI-PromptGenerator.exe  # File chính để chạy
├── ... (các file dependency)
```

## ⚠️ Lưu ý quan trọng:
1. **Bảo mật key**: Đừng chia sẻ key bản quyền của bạn
2. **File license**: File `license.dat` sẽ được tạo sau khi kích hoạt thành công
3. **Backup**: Luôn backup file `scenes.txt` gốc của bạn
4. **Output**: Kết quả được lưu trong `output_prompts.txt`

## 🛠️ Features:
- ✅ Hệ thống license key chuyên nghiệp
- ✅ Giao diện GUI thân thiện
- ✅ Tích hợp Google Gemini AI
- ✅ Hỗ trợ nhiều kiểu camera shot
- ✅ Tự động dịch tiếng Việt sang tiếng Anh
- ✅ Generate prompts chất lượng cao

## 📞 Hỗ trợ:
- Tool đã được đóng gói sẵn, chỉ cần chạy file .exe
- Hệ thống bản quyền bảo vệ khỏi việc sử dụng trái phép
- Giao diện GUI giúp dễ sử dụng cho người không chuyên

## 🔒 Bảo mật:
- Key được lưu trữ an toàn trong file `license.dat` ẩn
- Có thể mở rộng thêm kiểm tra online qua API
- Checksum để xác thực tính toàn vẹn của license