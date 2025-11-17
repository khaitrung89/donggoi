# 🎬 FilmAI Prompt Generator v2.0 - Enhanced Edition

## 🆕 PHIÊN BẢN MỚI - TÍNH NĂNG NỔI BẬT

### ✨ **Version 2.0 có gì mới?**

#### 1. **⚙️ Settings Dialog hoàn chỉnh**
- 🔑 **API Keys Management Tab**
  - Paste nhiều API keys cùng lúc từ clipboard
  - Validate format keys tự động
  - Hiển thị số lượng keys hợp lệ
  - Lưu tự động vào config.json

#### 2. **🌍 Configuration Tab**
- **World Type Selection:**
  - 🏙️ Modern (Hiện đại)
  - 🏰 Medieval (Trung cổ)
  - ✨ Fantasy (Phép thuật)

- **AI Model Selection:**
  - ⚡ Gemini 2.5 Flash (Nhanh, rẻ - khuyến nghị)
  - 🚀 Gemini 2.5 Flash-8B (Nhanh nhất)
  - 💎 Gemini 2.0 Flash Exp (Thử nghiệm)

- **Auto Options:**
  - ✅ Tự động dịch sang tiếng Việt sau khi generate
  - ✅ Tự động mở thư mục output khi hoàn thành

#### 3. **📁 Output Management**
- Chọn thư mục lưu output tùy ý
- Tùy chỉnh tên file output:
  - JSON output (Node 2)
  - English prompts
  - Vietnamese prompts
- Nút "Mở thư mục Output" để xem kết quả nhanh

#### 4. **🔄 Workflow tích hợp**
- **1 click chạy tất cả:**
  - Node 2: Generate JSON prompts
  - Node 3: Translate sang tiếng Việt
- Tự động copy outputs sang thư mục đã chọn
- Log chi tiết từng bước

#### 5. **💾 Config Management**
- Lưu settings vào `config.json`
- Tự động load settings lần sau
- Tương thích ngược với `api_keys.txt`

---

## 📊 SO SÁNH VERSION

| Tính năng | v1.0 (gui_app.py) | v2.0 (gui_app_enhanced.py) |
|-----------|-------------------|----------------------------|
| API Keys UI | ❌ Phải edit file txt | ✅ GUI quản lý đầy đủ |
| Paste từ clipboard | ❌ | ✅ |
| World Type selection | ❌ Hardcode | ✅ GUI chọn |
| Model selection | ❌ Hardcode | ✅ 3 models |
| Output directory | ❌ Cố định | ✅ Chọn tùy ý |
| Auto translate | ❌ Chạy riêng | ✅ Tích hợp 1 click |
| Config persistence | ❌ | ✅ Lưu config.json |
| License check | ✅ | ✅ |

---

## 🚀 HƯỚNG DẪN SỬ DỤNG

### **Lần đầu sử dụng:**

1. **Nhập License Key:**
   - Mở app lần đầu sẽ yêu cầu license
   - Nhập một trong các key mẫu:
     - `ABCD-EFGH-IJKL-MNOP`
     - `1234-5678-9012-3456`
     - `TEST-KEYS-2024-DEMO`

2. **Cấu hình Settings:**
   - Click nút **⚙️ Settings**

   **Tab 1: API Keys**
   - Paste các Gemini API keys (mỗi key 1 dòng)
   - Lấy key tại: https://aistudio.google.com/apikey
   - Click "💾 Lưu"

   **Tab 2: Cấu hình**
   - Chọn World Type phù hợp với kịch bản
   - Chọn AI Model (khuyến nghị: Gemini 2.5 Flash)
   - Tick ✅ "Tự động dịch..." và "Tự động mở..."

   **Tab 3: Output**
   - Click "📁 Chọn" để chọn thư mục lưu kết quả
   - (Tùy chọn) Đổi tên file output

3. **Generate Prompts:**
   - Click **📁 Chọn file** → chọn `scenes.txt`
   - Click **🚀 Bắt đầu Generate**
   - Đợi... (xem log để theo dõi)
   - Kết quả sẽ xuất hiện trong thư mục đã chọn:
     - `output_prompts.txt` (JSON)
     - `final_prompts_en.txt` (Tiếng Anh)
     - `final_prompts_vi.txt` (Tiếng Việt)

---

## 📁 CẤU TRÚC FILE MỚI

```
PHAN-III-Chat-AI-Final-Anh-CUOI-ko-MOTA-xe-cua/
├── gui_app.py                    # Version 1.0 (cũ)
├── gui_app_enhanced.py           # Version 2.0 (MỚI) ⭐
├── generate_prompts.py           # Node 2 core
├── translate_prompts.py          # Node 3 core
├── license_manager.py            # License system
├── config.json                   # Settings (auto-generated) 🆕
├── api_keys.txt                  # API keys backup
├── scenes.txt                    # Input scenes
├── character_dictionary.json
├── camera_styles.txt
├── extras_worlds.json
├── build.spec                    # PyInstaller config (v1)
├── build_enhanced.spec           # PyInstaller config (v2) 🆕
├── build_windows.bat             # Build script
└── README_V2.md                  # This file 🆕
```

---

## 🔧 BUILD .EXE VERSION 2.0

### **Build trên Windows:**

**Cách 1: Tự động**
```cmd
# Sẽ tạo file build script mới
build_enhanced.bat
```

**Cách 2: Manual**
```cmd
pip install pyinstaller google-generativeai
pyinstaller --clean --noconfirm build_enhanced.spec
```

**Output:**
```
dist/FilmAI-PromptGenerator-v2.exe
```

---

## ⚡ WORKFLOW MỚI

### **Workflow v1.0 (cũ):**
```
1. Chọn file scenes.txt
2. Chạy gui_app.py → output_prompts.txt
3. Chạy translate_prompts.py riêng
4. Kết quả ở thư mục hiện tại
```

### **Workflow v2.0 (mới):**
```
1. Settings một lần
2. Chọn file scenes.txt
3. Click "Bắt đầu Generate"
4. ✅ Auto: Generate + Translate + Save to custom folder
```

**Tiết kiệm:** ~50% thời gian thao tác!

---

## 🎯 TÍNH NĂNG CHI TIẾT

### **1. API Keys Management**

**Trước (v1.0):**
```
1. Mở Notepad
2. Edit api_keys.txt
3. Lưu file
4. Restart app
```

**Bây giờ (v2.0):**
```
1. Settings → API Keys tab
2. Paste tất cả keys cùng lúc
3. Click "Kiểm tra Keys" để validate
4. Lưu → Done!
```

**Format hỗ trợ:**
```
AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AIzaSyDyyyyyyyyyyyyyyyyyyyyyyyyyyyy
AIzaSyDzzzzzzzzzzzzzzzzzzzzzzzzzzzz
```

### **2. World Type System**

**Modern (Hiện đại):**
- Office workers, taxi drivers, police
- City streets, modern buildings
- Contemporary setting

**Medieval (Trung cổ):**
- Palace maids, castle guards, merchants
- Stone castles, villages, forests
- Historical fantasy

**Fantasy (Phép thuật):**
- Forest fairies, temple monks, sages
- Magic, mythical creatures
- High fantasy elements

### **3. Model Selection**

| Model | Speed | Cost | Quality | Use Case |
|-------|-------|------|---------|----------|
| Gemini 2.5 Flash | ⚡⚡⚡ | $ | ⭐⭐⭐ | Khuyến nghị chung |
| Gemini 2.5 Flash-8B | ⚡⚡⚡⚡ | $ | ⭐⭐ | Số lượng lớn, budget thấp |
| Gemini 2.0 Flash Exp | ⚡⚡ | $ | ⭐⭐⭐⭐ | Test tính năng mới |

### **4. Output Customization**

Có thể đặt tên file theo project:
```
project-alpha_prompts.txt
project-alpha_en.txt
project-alpha_vi.txt
```

Hoặc theo ngày:
```
output_2025-11-17.txt
final_en_2025-11-17.txt
final_vi_2025-11-17.txt
```

---

## 🐛 TROUBLESHOOTING

### **❌ Lỗi: "Chưa có API keys"**
→ Vào Settings → API Keys → Paste keys → Lưu

### **❌ Lỗi: "File không tồn tại"**
→ Kiểm tra đường dẫn file input đúng chưa

### **❌ Build .exe lỗi**
→ Xem `HUONG_DAN_BUILD_WINDOWS.md`

### **❌ App không lưu settings**
→ Kiểm tra quyền ghi file trong thư mục app

---

## 📚 COMPATIBILITY

### **Tương thích ngược:**
- ✅ Vẫn đọc được `api_keys.txt` cũ
- ✅ Vẫn chạy được với file config cũ
- ✅ Output format không đổi

### **Migration từ v1.0:**
1. Copy `api_keys.txt` sang thư mục mới
2. Chạy `gui_app_enhanced.py`
3. App sẽ tự động load API keys
4. Vào Settings kiểm tra lại

---

## 🔐 SECURITY NOTES

**v2.0 vẫn có issues giống v1.0:**
- ⚠️ License keys hardcoded
- ⚠️ API keys lưu plaintext trong config.json
- ⚠️ Cần encryption cho production

**Khuyến nghị:**
- Không share file config.json
- Không commit api_keys.txt lên git
- Build commercial cần thêm encryption

---

## 📞 SUPPORT

**Docs:**
- `HUONG_DAN_BUILD_WINDOWS.md` - Build instructions
- `CHANGES_AND_FIXES.md` - Bug fixes log
- `README.md` - Original v1.0 docs

**Issues:**
- GitHub Issues: https://github.com/khaitrung89/donggoi/issues

---

## 🎉 CHANGELOG

### **v2.0 (2025-11-17)**
- ➕ Settings Dialog với 3 tabs
- ➕ API Keys UI management
- ➕ World Type selection
- ➕ Model selection (3 models)
- ➕ Output directory picker
- ➕ Auto translate workflow
- ➕ Config persistence (config.json)
- ➕ Paste from clipboard
- ➕ API keys validation
- 🔧 Tích hợp Node 2 + Node 3

### **v1.0 (2025-11-16)**
- ✅ GUI cơ bản
- ✅ License system
- ✅ File picker
- ✅ Generate prompts

---

## 📄 LICENSE

MIT License - Free to use

---

**Version:** 2.0
**Last Updated:** 2025-11-17
**Author:** FilmAI Team + Claude AI Enhanced
