# ⚡ QUICKSTART - FilmAI v2.0

## 🚀 BẮT ĐẦU NHANH (5 PHÚT)

### **Bước 1: Chạy App** (30 giây)

```cmd
# Nếu có Python
python gui_app_enhanced.py

# Nếu có .exe
FilmAI-PromptGenerator-v2.exe
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

### **Bước 3: Generate** (2 phút)

1. Click **📁 Chọn file** → chọn `scenes.txt`
2. Click **🚀 Bắt đầu Generate**
3. ☕ Đợi... (xem log)

**→ Kết quả:**
```
📁 Output:
   ├── output_prompts.txt      (JSON)
   ├── final_prompts_en.txt    (English)
   └── final_prompts_vi.txt    (Vietnamese)
```

---

## 📝 FILE SCENES.TXT MẪU

```txt
Scene 1: Alex stands on a rooftop overlooking the city, his expression tense as he reviews the mission details on a holographic display.

Scene 2: Close-up of Maya's face as she reads an encrypted message, her eyes widening in surprise.

Scene 3: Marcus enters the abandoned warehouse cautiously, hand on his weapon.
```

---

## ⚙️ CÀI ĐẶT NÂNG CAO

### **Tab Configuration:**

**World Type:**
- 🏙️ Modern - Thế giới hiện đại
- 🏰 Medieval - Trung cổ
- ✨ Fantasy - Phép thuật

**AI Model:**
- ⚡ Gemini 2.5 Flash (khuyến nghị)

**Tùy chọn:**
- ✅ Tự động dịch sang tiếng Việt
- ✅ Tự động mở thư mục output

---

## 🎯 TIPS

### **Tối ưu tốc độ:**
- Dùng 5-10 API keys → xoay vòng tự động
- Chọn model Flash-8B nếu cần nhanh nhất

### **Tối ưu chất lượng:**
- Dùng model Gemini 2.0 Flash Exp
- Scene description chi tiết hơn

### **Batch processing:**
- Scenes nhỏ: 4-10 scenes → test
- Scenes lớn: 60+ scenes → production

---

## ❓ FAQ NHANH

**Q: File .exe ở đâu?**
A: Build trên Windows: `build_enhanced.bat`

**Q: Cần bao nhiêu API keys?**
A: Tối thiểu 1, khuyến nghị 5-10 keys

**Q: Có mất phí không?**
A: Free tier: 1500 requests/day/key

**Q: Output lưu ở đâu?**
A: Settings → Output → Chọn thư mục

**Q: Làm sao dịch sang tiếng Việt?**
A: Settings → Config → Tick ✅ "Tự động dịch"

---

## 🐛 SỬA LỖI NHANH

**Lỗi: "Chưa có API keys"**
```
→ Settings → API Keys → Paste keys → Lưu
```

**Lỗi: "Invalid API key"**
```
→ Kiểm tra key tại: https://aistudio.google.com/apikey
→ Key phải bắt đầu với: AIza...
```

**Lỗi: App không lưu settings**
```
→ Chạy app with admin rights (Windows)
→ Kiểm tra quyền ghi file config.json
```

---

## 📚 ĐỌC THÊM

- 📘 **README_V2.md** - Tài liệu đầy đủ
- 📘 **HUONG_DAN_BUILD_WINDOWS.md** - Build .exe
- 📘 **CHANGES_AND_FIXES.md** - Bug fixes

---

**That's it! Enjoy! 🎉**
