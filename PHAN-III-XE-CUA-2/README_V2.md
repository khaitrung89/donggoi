# 🎬 FilmAI XE-CUA-2 v2.0 - Enhanced Edition

## 🆕 WORKFLOW ĐẦY ĐỦ 5 BƯỚC

Hệ thống tạo phim AI hoàn chỉnh từ ý tưởng đến prompts với GUI enhanced!

---

## 📊 WORKFLOW TỔNG QUAN

```
story_idea.txt (Ý tưởng + Thế giới + Nhân vật)
    ↓
[BƯỚC 1] generate_chapters_from_idea.py
    ↓
chapters.txt (Chapters EN)
    ↓
[BƯỚC 2] generate_scenes_from_chapters.py
    ↓
scenes.txt (Scenes EN)
    ↓
[BƯỚC 3] generate_prompts.py
    ↓
output_prompts.txt (JSON EN)
    ↓
[BƯỚC 4] postprocess_output_prompts.py
    ↓
output_prompts_clean.txt (JSON EN - Chuẩn)
    ↓
[BƯỚC 5] translate_prompts.py
    ↓
final_prompts_en.txt + final_prompts_vi.txt
```

---

## ✨ PHIÊN BẢN V2.0 - TÍNH NĂNG MỚI

### **1. ⚙️ Settings Dialog (3 Tabs)**

**🔑 API Keys Tab:**
- Paste nhiều keys cùng lúc từ clipboard
- Validate format tự động
- Hiển thị số keys hợp lệ/không hợp lệ

**⚙️ Configuration Tab:**
- **Model Selection:**
  - Gemini 2.5 Flash (khuyến nghị)
  - Gemini 2.5 Flash-8B
  - Gemini 2.0 Flash Exp

- **Auto Options:**
  - Tự động chạy tất cả 5 bước
  - Tự động mở thư mục output
  - Target chapters (6-12)
  - Target scenes (40/70/100+)

**📁 Output Tab:**
- Chọn thư mục lưu output
- Tùy chỉnh tên file output

### **2. 🔄 Workflow Tích Hợp**

**Option A: Chạy toàn bộ (1 click)**
- Từ story_idea.txt → final outputs (EN + VI)
- Tự động chạy cả 5 bước liên tiếp
- Log chi tiết từng bước

**Option B: Chạy từng bước riêng**
- Chọn bước bắt đầu:
  - Từ bước 1 (story_idea.txt)
  - Từ bước 2 (chapters.txt)
  - Từ bước 3 (scenes.txt)
  - Từ bước 4 (output_prompts.txt)
  - Chỉ bước 5 (translate)

### **3. 💾 Config Management**

- Lưu tất cả settings vào `config.json`
- Auto-load khi mở app lần sau
- Tương thích với `api_keys.txt`

### **4. 🔐 License System**

- Check license khi khởi động
- Popup nhập key bản quyền
- License keys mẫu: `ABCD-EFGH-IJKL-MNOP`

---

## 📁 CẤU TRÚC FILE

```
PHAN-III-XE-CUA-2/
├── gui_app_enhanced.py           # GUI v2.0 ⭐
├── gui_app.py                    # GUI v1.0 (cũ)
│
├── generate_chapters_from_idea.py
├── generate_scenes_from_chapters.py
├── generate_prompts.py
├── postprocess_output_prompts.py
├── translate_prompts.py
│
├── build_enhanced.spec           # Build config v2.0 🆕
├── build_enhanced.bat            # Build script v2.0 🆕
│
├── config.json                   # Settings (auto) 🆕
├── api_keys.txt
├── license_manager.py
│
├── story_idea.txt                # Input: Ý tưởng
├── chapters.txt                  # Bước 1 → 2
├── scenes.txt                    # Bước 2 → 3
├── output_prompts.txt            # Bước 3 → 4
├── output_prompts_clean.txt      # Bước 4 → 5
├── final_prompts_en.txt          # Output EN
└── final_prompts_vi.txt          # Output VI
```

---

## 🚀 CÁCH SỬ DỤNG

### **Quick Start (5 phút):**

#### **1. Chạy App**
```bash
python gui_app_enhanced.py
```

#### **2. Nhập License**
```
ABCD-EFGH-IJKL-MNOP
```

#### **3. Settings**
- Click **⚙️ Settings**
- **API Keys tab:** Paste các Gemini API keys
- **Configuration tab:** Chọn model & options
- **Output tab:** Chọn thư mục lưu
- Click **💾 Lưu**

#### **4. Chuẩn bị Input**

Tạo/Edit `story_idea.txt`:
```
TITLE: Hành Trình Của Lana
WORLD: Medieval Fantasy
ACTS: 3
TARGET_CHAPTERS: 8

CHARACTERS:
- Lana: Nữ chiến binh trẻ...
- Adai: Pháp sư già...
- Asuka: Cung thủ...

STORY:
Act 1: Lana khám phá...
Act 2: Cuộc chiến...
Act 3: Kết thúc...
```

#### **5. Generate**
- Click **🚀 Bắt đầu Full Workflow**
- Hoặc chọn **Start From:** để bắt đầu từ bước cụ thể
- ☕ Đợi... (xem log)

#### **6. Kết Quả**
```
📁 Output Folder:
   ├── chapters.txt
   ├── scenes.txt
   ├── output_prompts_clean.txt
   ├── final_prompts_en.txt    ← Dùng cho AI Video
   └── final_prompts_vi.txt    ← Dùng cho phụ đề/voice
```

---

## 📊 SO SÁNH v1.0 vs v2.0

| Tính năng | v1.0 | v2.0 Enhanced |
|-----------|------|---------------|
| **GUI** | ✅ Basic | ✅ Advanced với Settings |
| **API Keys UI** | ❌ Edit txt | ✅ Paste từ clipboard |
| **Workflow** | ❌ Chạy riêng từng bước | ✅ 1-click full workflow |
| **Step Selector** | ❌ | ✅ Chọn bước bắt đầu |
| **Config Save** | ❌ | ✅ config.json |
| **Output Picker** | ❌ Cố định | ✅ Chọn thư mục |
| **Auto Translate** | ❌ Chạy riêng | ✅ Tích hợp |
| **Progress Log** | ✅ | ✅ Chi tiết hơn |
| **License** | ✅ | ✅ |

---

## 🔧 BUILD .EXE (Windows)

### **Cách 1: Tự động**
```cmd
build_enhanced.bat
```

### **Cách 2: Manual**
```cmd
pip install pyinstaller google-generativeai
pyinstaller --clean --noconfirm build_enhanced.spec
```

**Output:**
```
dist/FilmAI-XE-CUA-2-v2.exe
```

---

## 📖 CÁC WORKFLOW SCENARIOS

### **Scenario 1: Tạo phim mới từ đầu**
```
1. Viết story_idea.txt
2. Click "🚀 Full Workflow (All Steps)"
3. Đợi ~10-30 phút (tùy độ dài)
4. Lấy final_prompts_en.txt → AI Video
```

### **Scenario 2: Đã có chapters, muốn tạo scenes**
```
1. Có sẵn chapters.txt
2. Chọn "Start From: Step 2 (Chapters → Scenes)"
3. Click "🚀 Bắt đầu"
4. Lấy scenes.txt + final outputs
```

### **Scenario 3: Chỉ muốn dịch lại**
```
1. Có sẵn output_prompts_clean.txt
2. Chọn "Start From: Step 5 (Translate Only)"
3. Click "🚀 Bắt đầu"
4. Lấy final_prompts_vi.txt mới
```

### **Scenario 4: Test nhanh**
```
1. Dùng story_idea.txt ngắn (3 chapters, 12 scenes)
2. Full Workflow
3. Check kết quả trong ~5 phút
```

---

## ⚙️ CẤU HÌNH NÂNG CAO

### **Target Chapters/Scenes:**

**Settings → Configuration:**
```
Target Chapters: 6-12 (khuyến nghị 8)
Target Scenes:
  - 40 scenes: Phim ngắn (~20 phút)
  - 70 scenes: Phim trung bình (~35 phút)
  - 100+ scenes: Phim dài (~50 phút+)
```

### **Model Selection:**

| Model | Speed | Cost | Quality | Use Case |
|-------|-------|------|---------|----------|
| Gemini 2.5 Flash | ⚡⚡⚡ | $ | ⭐⭐⭐ | Production |
| Gemini 2.5 Flash-8B | ⚡⚡⚡⚡ | $ | ⭐⭐ | Rapid prototyping |
| Gemini 2.0 Flash Exp | ⚡⚡ | $ | ⭐⭐⭐⭐ | Experimental |

---

## 🎯 NGÔN NGỮ Ở TỪNG BƯỚC

### **Zone 1: Input**
- `story_idea.txt`: Tiếng Việt/Anh/Mixed OK
- Tool sẽ tự chuyển sang EN từ bước 1

### **Zone 2: Processing (EN Only)**
- `chapters.txt`: English
- `scenes.txt`: English
- `output_prompts.txt`: English
- `output_prompts_clean.txt`: English (chuẩn)

### **Zone 3: Output (EN + VI)**
- `final_prompts_en.txt`: English (cho AI Video)
- `final_prompts_vi.txt`: Vietnamese (cho phụ đề/voice)

---

## 🐛 TROUBLESHOOTING

### **Lỗi: "Chưa có API keys"**
→ Settings → API Keys → Paste keys → Lưu

### **Lỗi: "File story_idea.txt not found"**
→ Tạo file story_idea.txt trong thư mục tool

### **Lỗi: Workflow dừng ở bước 2**
→ Check log, có thể do API quota hết → thêm keys

### **App chậm**
→ Chọn model Flash-8B, giảm số chapters/scenes

---

## 📚 TÀI LIỆU THAM KHẢO

- **MO-HINH.txt** - Workflow chi tiết 5 bước
- **README.md** - Tài liệu v1.0 gốc
- **BUILD_INSTRUCTIONS.md** - Hướng dẫn build

---

## 🎉 HIGHLIGHTS v2.0

### **Tính năng nổi bật:**

1. **🔄 1-Click Full Workflow**
   - Chạy cả 5 bước tự động
   - Không cần chạy script riêng lẻ

2. **📋 Workflow Selector**
   - Bắt đầu từ bất kỳ bước nào
   - Tiết kiệm thời gian khi test

3. **⚙️ Settings UI**
   - API Keys management
   - Model selection
   - Output configuration

4. **📁 Smart Output**
   - Tự tạo thư mục
   - Copy files vào thư mục chọn
   - Tổ chức rõ ràng

---

## 💡 TIPS & BEST PRACTICES

### **Optimize Workflow:**
```
1. Test với story ngắn trước (3 chapters, 12 scenes)
2. Check output quality
3. Adjust settings nếu cần
4. Scale lên production (8 chapters, 60 scenes)
```

### **API Keys Management:**
```
- Dùng 5-10 keys để tránh quota limit
- Tool sẽ tự động xoay vòng
- Monitor usage tại: https://aistudio.google.com
```

### **Quality Control:**
```
- Review chapters.txt sau bước 1
- Review scenes.txt sau bước 2
- Adjust nếu cần rồi mới chạy tiếp
```

---

## 📄 LICENSE

MIT License - Free to use

---

## 📞 SUPPORT

**Files:**
- README_V2.md - This file
- MO-HINH.txt - Workflow details
- Build instructions - Trong BUILD_INSTRUCTIONS.md

**GitHub:**
- Repository: https://github.com/khaitrung89/donggoi

---

**Version:** 2.0 Enhanced
**Last Updated:** 2025-11-17
**Author:** FilmAI Team + Claude AI

**🎬 Tạo phim AI chưa bao giờ dễ dàng đến thế! 🚀**
