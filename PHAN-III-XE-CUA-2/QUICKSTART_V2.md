# ⚡ QUICKSTART - FilmAI XE-CUA-2 v2.0

## 🚀 BẮT ĐẦU NHANH (10 PHÚT)

### **Bước 1: Chạy App** (30 giây)

```bash
# Nếu có Python
python gui_app_enhanced.py

# Nếu có .exe
FilmAI-XE-CUA-2-v2.exe
```

**→ Nhập License Key:**
```
ABCD-EFGH-IJKL-MNOP
```

---

### **Bước 2: Settings** (2 phút)

Click **⚙️ Settings** → Tab **🔑 API Keys**

**Paste API keys** (mỗi key 1 dòng):
```
AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AIzaSyDyyyyyyyyyyyyyyyyyyyyyyyyyyyy
AIzaSyDzzzzzzzzzzzzzzzzzzzzzzzzzzzz
```

**Lấy API key tại:** https://aistudio.google.com/apikey

Click **"💾 Lưu"**

---

### **Bước 3: Chuẩn bị Story Idea** (3 phút)

Tạo/Edit file `story_idea.txt`:

```
TITLE: Hành Trình Của Lana
WORLD: Medieval Fantasy
GENRE: Action, Adventure
ACTS: 3
TARGET_CHAPTERS: 8
TARGET_SCENES: 60

MAIN CHARACTERS:
- Lana: 22-year-old warrior princess with silver hair...
- Adai: 65-year-old wise mage with gray beard...
- Asuka: 28-year-old skilled archer with blonde hair...

STORY SUMMARY:
Act 1: Lana discovers her destiny...
Act 2: The battle against dark forces...
Act 3: Final confrontation and resolution...

THEMES: Courage, friendship, sacrifice
TONE: Epic, emotional, inspiring
```

---

### **Bước 4: Generate** (5-30 phút)

#### **Option A: Full Workflow (Toàn bộ 5 bước)**
1. Click **🚀 Bắt đầu Full Workflow**
2. ☕ Đợi... Tool sẽ tự chạy:
   ```
   Step 1: Idea → Chapters
   Step 2: Chapters → Scenes
   Step 3: Scenes → Prompts
   Step 4: Postprocess
   Step 5: Translate
   ```

#### **Option B: Từng bước riêng**
```
🔹 Đã có chapters.txt?
→ Chọn "Start From: Step 2"

🔹 Đã có scenes.txt?
→ Chọn "Start From: Step 3"

🔹 Chỉ muốn dịch lại?
→ Chọn "Start From: Step 5"
```

---

### **Bước 5: Xem Kết Quả** (1 phút)

Click **📁 Mở thư mục Output**

**Files được tạo:**
```
📁 Output:
├── chapters.txt                  (8 chapters)
├── scenes.txt                    (60 scenes)
├── output_prompts.txt            (JSON thô)
├── output_prompts_clean.txt      (JSON chuẩn)
├── final_prompts_en.txt          ← 🎬 Dùng cho AI Video
└── final_prompts_vi.txt          ← 📝 Dùng cho phụ đề/voice
```

**→ Lấy `final_prompts_en.txt` nạp vào:**
- VEO / Sora / Dreamina
- Runway / Pika / Kling

---

## 📊 WORKFLOW 5 BƯỚC

```
[Input]
story_idea.txt
   ↓
[BƯỚC 1] Generate Chapters (1-2 phút)
chapters.txt
   ↓
[BƯỚC 2] Generate Scenes (3-5 phút)
scenes.txt
   ↓
[BƯỚC 3] Generate Prompts (10-20 phút)
output_prompts.txt
   ↓
[BƯỚC 4] Postprocess (1 phút)
output_prompts_clean.txt
   ↓
[BƯỚC 5] Translate (5-10 phút)
   ↓
[Output]
final_prompts_en.txt + final_prompts_vi.txt
```

**Tổng thời gian:** 20-40 phút (tùy độ dài)

---

## 🎯 CẤU HÌNH NHANH

### **Settings → Configuration:**

**Target Chapters:**
```
- Small project: 4-6 chapters
- Medium project: 8-10 chapters
- Large project: 12+ chapters
```

**Target Scenes:**
```
- Short film: 20-40 scenes (~10-20 phút)
- Medium film: 60-80 scenes (~30-40 phút)
- Long film: 100+ scenes (~50+ phút)
```

**Model:**
```
⚡ Gemini 2.5 Flash      → Khuyến nghị (cân bằng tốc độ/chất lượng)
🚀 Gemini 2.5 Flash-8B   → Nhanh nhất (test/prototype)
💎 Gemini 2.0 Flash Exp  → Chất lượng cao (production)
```

---

## ❓ FAQ NHANH

**Q: Bao lâu để tạo 1 phim?**
A:
- Short (20 scenes): ~15 phút
- Medium (60 scenes): ~30 phút
- Long (100 scenes): ~60 phút

**Q: Cần bao nhiêu API keys?**
A: 5-10 keys (tool tự xoay vòng)

**Q: Chi phí?**
A: Free tier: 1500 requests/day/key = ~300-500 scenes/day

**Q: File output ở đâu?**
A: Settings → Output → Chọn thư mục

**Q: Chạy lại 1 bước được không?**
A: Được! Chọn "Start From: Step X"

**Q: Làm sao biết đang chạy bước nào?**
A: Xem Log area → hiển thị từng bước

---

## 🔧 TEST NHANH

### **Story idea test ngắn:**

```
TITLE: Test Story
ACTS: 3
TARGET_CHAPTERS: 3
TARGET_SCENES: 12

CHARACTERS:
- Hero: Main character
- Guide: Mentor

STORY:
Act 1: Beginning
Act 2: Challenge
Act 3: Resolution
```

**→ Chạy Full Workflow → ~5 phút**

---

## 🐛 SỬA LỖI NHANH

**Lỗi: "story_idea.txt not found"**
```
→ Tạo file story_idea.txt trong thư mục tool
```

**Lỗi: "API key invalid"**
```
→ Check keys tại: https://aistudio.google.com/apikey
→ Paste lại trong Settings
```

**Lỗi: Dừng đột ngột**
```
→ Check log xem bước nào lỗi
→ Có thể quota hết → thêm API keys
```

**App chậm**
```
→ Giảm số chapters/scenes
→ Hoặc chọn model Flash-8B
```

---

## 📚 ĐỌC THÊM

- 📘 **README_V2.md** - Tài liệu đầy đủ
- 📘 **MO-HINH.txt** - Workflow chi tiết
- 📘 **BUILD_INSTRUCTIONS.md** - Build .exe

---

## 💡 TIPS PRO

### **Optimize Workflow:**
```
1. Test ngắn trước (3 chapters, 12 scenes)
2. Review quality
3. Adjust settings
4. Scale to production
```

### **Quality Control:**
```
- Review chapters.txt sau Step 1
- Edit nếu cần rồi chạy tiếp từ Step 2
- Không cần chạy lại toàn bộ!
```

### **Save Time:**
```
- Lưu story_idea.txt templates
- Reuse characters & worlds
- Batch process nhiều stories
```

---

**That's it! Happy filmmaking! 🎬✨**
