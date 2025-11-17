# 📥 HƯỚNG DẪN TẢI VÀ SỬ DỤNG FILMAI XE-CUA-2 v2.0

## 📋 MỤC LỤC

1. [Tải về thư mục](#bước-1-tải-zip-từ-github)
2. [Giải nén và dọn dẹp](#bước-2-giải-nén-file-zip)
3. [Cài đặt Python và dependencies](#bước-3-cài-đặt-python)
4. [Chạy ứng dụng](#bước-4-chạy-ứng-dụng)
5. [Cấu hình Settings](#bước-5-cấu-hình-settings)
6. [Tạo phim đầu tiên](#bước-6-tạo-phim-đầu-tiên)
7. [Troubleshooting](#troubleshooting)

---

## 📥 PHẦN 1: TẢI VỀ VÀ CÀI ĐẶT

### **BƯỚC 1: TẢI ZIP TỪ GITHUB**

#### **1.1. Mở trình duyệt web và vào link:**

```
https://github.com/khaitrung89/donggoi/tree/claude/review-chat-ai-project-01X3iAF6xMqCiN2SKigxfVC6
```

#### **1.2. Tải file ZIP:**

```
┌─────────────────────────────────────┐
│                                     │
│  1. Tìm nút "Code" (màu xanh lá)   │
│  2. Click vào nút "Code"           │
│  3. Chọn "Download ZIP"             │
│                                     │
│  ┌───────────────────┐             │
│  │  Code ▼           │             │
│  ├───────────────────┤             │
│  │ Clone             │             │
│  │ HTTPS             │             │
│  │ SSH               │             │
│  ├───────────────────┤             │
│  │ Download ZIP  ◄───┼─── CLICK   │
│  └───────────────────┘             │
│                                     │
└─────────────────────────────────────┘
```

#### **1.3. File sẽ tải về:**

**Tên file:**
```
donggoi-claude-review-chat-ai-project-01X3iAF6xMqCiN2SKigxfVC6.zip
```

**Kích thước:** ~5-10 MB

**Nơi lưu:** Thư mục Downloads của bạn

---

### **BƯỚC 2: GIẢI NÉN FILE ZIP**

#### **2.1. Cách giải nén:**

**Trên Windows:**
```
1. Tìm file ZIP trong thư mục Downloads
2. Chuột phải vào file
3. Chọn "Extract All..." (hoặc "Giải nén tất cả...")
4. Chọn vị trí giải nén (ví dụ: Desktop)
5. Click "Extract" (Giải nén)
```

**Trên Mac:**
```
1. Tìm file ZIP trong Downloads
2. Double-click vào file
3. File sẽ tự động giải nén
```

**Trên Linux:**
```bash
cd ~/Downloads
unzip donggoi-claude-review-chat-ai-project-01X3iAF6xMqCiN2SKigxfVC6.zip
```

#### **2.2. Sau khi giải nén:**

Bạn sẽ có thư mục với cấu trúc:
```
donggoi-claude-review-chat-ai-project-01X3iAF6xMqCiN2SKigxfVC6/
│
├── PHAN-III-Chat-AI-Final-Anh-CUOI-ko-MOTA-xe-cua/   ← Thư mục 1
│
├── PHAN-III-XE-CUA-2/                                ← Thư mục 2 (CẦN DÙNG)
│
└── (các file khác...)
```

---

### **BƯỚC 3: CHỈ GIỮ LẠI THƯ MỤC XE-CUA-2**

#### **Cách 1: Di chuyển ra ngoài (Khuyến nghị)** ⭐

**Windows:**
```
1. Mở thư mục: donggoi-claude-review-chat-ai-project-01X3iAF6xMqCiN2SKigxfVC6
2. Tìm thư mục: PHAN-III-XE-CUA-2
3. Click chuột phải → Cut (hoặc Ctrl+X)
4. Ra thư mục Desktop hoặc Documents
5. Click chuột phải → Paste (hoặc Ctrl+V)
6. Xóa thư mục gốc: donggoi-claude-review-chat-ai-project-01X3iAF6xMqCiN2SKigxfVC6
```

**Mac:**
```
1. Mở Finder
2. Vào thư mục Downloads
3. Mở: donggoi-claude-review-chat-ai-project-01X3iAF6xMqCiN2SKigxfVC6
4. Kéo thư mục PHAN-III-XE-CUA-2 ra Desktop
5. Xóa thư mục gốc
```

**Linux:**
```bash
# Di chuyển XE-CUA-2 ra Desktop
mv ~/Downloads/donggoi-claude-review-chat-ai-project-01X3iAF6xMqCiN2SKigxfVC6/PHAN-III-XE-CUA-2 ~/Desktop/

# Xóa thư mục gốc
rm -rf ~/Downloads/donggoi-claude-review-chat-ai-project-01X3iAF6xMqCiN2SKigxfVC6
```

#### **Cách 2: Đổi tên thư mục cho ngắn gọn**

```
Từ: PHAN-III-XE-CUA-2
Thành: XE-CUA-2
hoặc: FilmAI
```

#### **Kết quả cuối cùng:**

Bạn sẽ có thư mục sạch sẽ tại Desktop:

```
📁 XE-CUA-2/  (hoặc PHAN-III-XE-CUA-2)
   │
   ├── 📄 gui_app_enhanced.py           ⭐ File chính v2.0
   ├── 📄 gui_app.py                    (v1.0 - backup)
   │
   ├── 📄 build_enhanced.spec
   ├── 📄 build_enhanced.bat
   │
   ├── 📘 README_V2.md                  Tài liệu v2.0
   ├── 📘 QUICKSTART_V2.md              Quick start
   ├── 📘 SUMMARY_V2_UPGRADE.md         Tổng kết
   ├── 📘 MO-HINH.txt                   Workflow
   ├── 📘 HUONG_DAN_TAI_VA_SU_DUNG.md   File này
   │
   ├── 🐍 generate_chapters_from_idea.py
   ├── 🐍 generate_scenes_from_chapters.py
   ├── 🐍 generate_prompts.py
   ├── 🐍 postprocess_output_prompts.py
   ├── 🐍 translate_prompts.py
   │
   ├── 📝 api_keys.txt
   ├── 📝 story_idea.txt
   ├── 🔐 license_manager.py
   │
   └── ... (các file khác)
```

---

### **BƯỚC 4: CÀI ĐẶT PYTHON**

#### **4.1. Kiểm tra Python đã cài chưa:**

**Windows:**
```cmd
1. Mở Command Prompt (Tìm "cmd" trong Start Menu)
2. Gõ: python --version
3. Nhấn Enter
```

**Mac/Linux:**
```bash
python3 --version
```

#### **4.2. Nếu chưa có Python:**

**Windows:**
```
1. Vào: https://www.python.org/downloads/
2. Tải "Python 3.11" hoặc mới hơn
3. Chạy file cài đặt
4. ⚠️ QUAN TRỌNG: Tick ☑️ "Add Python to PATH"
5. Click "Install Now"
```

**Mac:**
```bash
# Cài Homebrew (nếu chưa có)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Cài Python
brew install python
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip
```

#### **4.3. Cài đặt dependencies:**

**Mở Command Prompt/Terminal trong thư mục XE-CUA-2:**

**Windows:**
```
1. Vào thư mục XE-CUA-2
2. Gõ "cmd" trong thanh địa chỉ
3. Nhấn Enter
4. Gõ lệnh:
```

```cmd
pip install google-generativeai
```

**Mac/Linux:**
```bash
cd ~/Desktop/XE-CUA-2
pip3 install google-generativeai
```

**Đợi cài đặt xong (~30 giây - 1 phút)**

---

## 🚀 PHẦN 2: CHẠY ỨNG DỤNG

### **BƯỚC 5: CHẠY GUI V2.0**

#### **5.1. Trong Command Prompt/Terminal, gõ:**

**Windows:**
```cmd
python gui_app_enhanced.py
```

**Mac/Linux:**
```bash
python3 gui_app_enhanced.py
```

#### **5.2. Cửa sổ GUI sẽ mở:**

```
┌─────────────────────────────────────┐
│  🔐 KÍCH HOẠT BẢN QUYỀN             │
├─────────────────────────────────────┤
│                                     │
│  Vui lòng nhập key bản quyền:      │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ XXXX-XXXX-XXXX-XXXX         │   │
│  └─────────────────────────────┘   │
│                                     │
│      [   Kích hoạt   ]             │
│                                     │
└─────────────────────────────────────┘
```

#### **5.3. Nhập License Key mẫu:**

Chọn một trong các key sau:

```
ABCD-EFGH-IJKL-MNOP
1234-5678-9012-3456
TEST-KEYS-2024-DEMO
PROD-UCTI-ONKE-Y2024
```

**Ví dụ:**
```
┌─────────────────────────────────┐
│  ABCD-EFGH-IJKL-MNOP            │
└─────────────────────────────────┘
```

**Click "Kích hoạt"**

#### **5.4. Cửa sổ chính sẽ hiện:**

```
┌──────────────────────────────────────────────────┐
│  🎬 FilmAI Prompt Generator v2.0                 │
├──────────────────────────────────────────────────┤
│                                                  │
│  📥 File Input (scenes.txt)                      │
│  ┌────────────────────────────┐  [📁 Chọn file] │
│  │                            │                  │
│  └────────────────────────────┘                  │
│                                                  │
│  📤 Thư mục Output                               │
│  📁 C:\Users\...\XE-CUA-2                       │
│                                                  │
│  [⚙️ Settings] [🚀 Bắt đầu] [⏹️ Dừng]          │
│                                                  │
│  ┌─ 📋 Tiến trình chạy ─────────────────────┐  │
│  │                                           │  │
│  │  ✅ Sẵn sàng                              │  │
│  │                                           │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│                                    [❌ Thoát]   │
└──────────────────────────────────────────────────┘
```

---

### **BƯỚC 6: CẤU HÌNH SETTINGS**

#### **6.1. Click nút "⚙️ Settings"**

Cửa sổ Settings sẽ mở với 3 tabs:

```
┌─────────────────────────────────────────┐
│  ⚙️ Cài đặt - Settings                  │
├─────────────────────────────────────────┤
│  [🔑 API Keys] [⚙️ Cấu hình] [📁 Output]│
├─────────────────────────────────────────┤
│                                         │
│  📝 Nhập các Gemini API Keys:          │
│  (mỗi key một dòng)                     │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ AIzaSyDxxxxxxxxxxxxxxxxxx       │   │
│  │ AIzaSyDyyyyyyyyyyyyyyyyyy       │   │
│  │ AIzaSyDzzzzzzzzzzzzzzzzzz       │   │
│  │                                 │   │
│  └─────────────────────────────────┘   │
│                                         │
│  [📋 Paste] [🗑️ Xóa] [✅ Kiểm tra]    │
│                                         │
│              [💾 Lưu] [❌ Hủy]         │
└─────────────────────────────────────────┘
```

#### **6.2. Tab "🔑 API Keys"**

**Lấy API Keys:**

1. Vào: https://aistudio.google.com/apikey
2. Đăng nhập Google
3. Click "Create API Key" hoặc "Get API Key"
4. Copy key (dạng: AIzaSyD...)
5. Lặp lại để tạo 5-10 keys

**Nhập vào Settings:**

**Cách 1: Paste từ clipboard (Khuyến nghị)**
```
1. Copy tất cả keys từ Google AI Studio
2. Click nút "📋 Paste từ Clipboard"
3. Keys sẽ tự động điền vào
```

**Cách 2: Gõ thủ công**
```
1. Paste từng key vào text area
2. Mỗi key một dòng:

AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AIzaSyDyyyyyyyyyyyyyyyyyyyyyyyyyyyy
AIzaSyDzzzzzzzzzzzzzzzzzzzzzzzzzzzz
```

**Click "✅ Kiểm tra Keys"**
```
Kết quả: ✅ Tìm thấy 3/3 keys hợp lệ
```

#### **6.3. Tab "⚙️ Cấu hình"**

```
┌─────────────────────────────────────────┐
│  🌍 World Type (Thể loại thế giới)      │
│  ○ 🏙️ Modern (Hiện đại)                 │
│  ● 🏰 Medieval (Trung cổ)               │
│  ○ ✨ Fantasy (Phép thuật)              │
│                                         │
│  🤖 AI Model                            │
│  ● ⚡ Gemini 2.5 Flash (Nhanh, rẻ)     │
│  ○ 🚀 Gemini 2.5 Flash-8B               │
│  ○ 💎 Gemini 2.0 Flash Exp              │
│                                         │
│  🔧 Tùy chọn khác                       │
│  ☑️ Tự động dịch sang tiếng Việt       │
│  ☐ Tự động mở file output               │
│                                         │
└─────────────────────────────────────────┘
```

**Chọn theo nhu cầu:**

- **World Type:** Tùy kịch bản của bạn
- **Model:** Khuyến nghị Gemini 2.5 Flash
- **Tùy chọn:** Tick ✅ "Tự động dịch..."

#### **6.4. Tab "📁 Output"**

```
┌─────────────────────────────────────────┐
│  📂 Thư mục lưu kết quả                 │
│                                         │
│  ┌────────────────────┐  [📁 Chọn]     │
│  │ C:\...\XE-CUA-2    │                │
│  └────────────────────┘                │
│                                         │
│  📝 Tên file output                     │
│                                         │
│  JSON output:                           │
│  ┌────────────────────────────────┐    │
│  │ output_prompts.txt             │    │
│  └────────────────────────────────┘    │
│                                         │
│  English output:                        │
│  ┌────────────────────────────────┐    │
│  │ final_prompts_en.txt           │    │
│  └────────────────────────────────┘    │
│                                         │
│  Vietnamese output:                     │
│  ┌────────────────────────────────┐    │
│  │ final_prompts_vi.txt           │    │
│  └────────────────────────────────┘    │
│                                         │
└─────────────────────────────────────────┘
```

**Click "📁 Chọn" để chọn thư mục lưu (nếu muốn)**

Mặc định: Thư mục hiện tại (XE-CUA-2)

#### **6.5. Click "💾 Lưu"**

Settings sẽ được lưu vào file `config.json`

---

## 🎬 PHẦN 3: TẠO PHIM ĐẦU TIÊN

### **BƯỚC 7: CHUẨN BỊ STORY IDEA**

#### **7.1. Tạo file `story_idea.txt`**

**Cách 1: Dùng Notepad (Windows)**
```
1. Mở Notepad
2. Copy nội dung bên dưới
3. Save As → story_idea.txt
4. Lưu vào thư mục XE-CUA-2
```

**Cách 2: Dùng Text Editor (Mac/Linux)**
```bash
cd ~/Desktop/XE-CUA-2
nano story_idea.txt
```

#### **7.2. Nội dung mẫu:**

```
TITLE: Hành Trình Của Lana
WORLD: Medieval Fantasy
GENRE: Action, Adventure, Drama
ACTS: 3
TARGET_CHAPTERS: 6
TARGET_SCENES: 40

=== MAIN CHARACTERS ===

1. LANA
- Age: 22 years old
- Role: Warrior Princess
- Appearance: Silver-haired young woman with piercing blue eyes,
  athletic build, wearing enchanted armor with royal insignia
- Personality: Brave, determined, compassionate
- Background: Exiled princess seeking to reclaim her kingdom

2. ADAI
- Age: 65 years old
- Role: Wise Mage, Mentor
- Appearance: Elderly man with long gray beard, wearing dark blue robes
  covered in mystical symbols, carrying ancient wooden staff
- Personality: Wise, patient, mysterious
- Background: Former royal advisor, now guardian of ancient magic

3. ASUKA
- Age: 28 years old
- Role: Skilled Archer, Loyal Friend
- Appearance: Blonde-haired woman with green eyes, lean and agile,
  dressed in forest-green hunting attire with bow and quiver
- Personality: Sharp-witted, loyal, cautious
- Background: Former royal guard, expert tracker

=== STORY SUMMARY ===

ACT 1: THE BEGINNING (Chapters 1-2)
Lana discovers she is the rightful heir to the throne after her
kingdom falls to dark forces. She meets Adai who reveals her destiny
and begins training her in combat and magic. Asuka joins their quest,
bringing crucial knowledge about the enemy.

ACT 2: THE JOURNEY (Chapters 3-4)
The trio embarks on a dangerous journey through enchanted forests
and ancient ruins to gather three magical artifacts needed to defeat
the dark lord. They face numerous challenges including mythical
creatures, betrayal, and internal conflicts that test their bonds.

ACT 3: THE FINAL BATTLE (Chapters 5-6)
With all artifacts gathered, Lana must lead an army of rebels against
the dark forces. The final confrontation reveals shocking truths about
her family's past. Lana must make the ultimate sacrifice to save her
kingdom and restore peace to the land.

=== THEMES ===
- Courage in the face of overwhelming odds
- The power of friendship and loyalty
- Sacrifice for the greater good
- Redemption and forgiveness
- The burden of leadership

=== TONE ===
Epic, emotional, inspiring with moments of humor and tenderness

=== VISUAL STYLE ===
Cinematic fantasy with realistic lighting, medieval architecture mixed
with magical elements, rich color palette emphasizing blues, silvers,
and forest greens
```

**Lưu file** (Ctrl+S hoặc Cmd+S)

---

### **BƯỚC 8: CHẠY WORKFLOW**

#### **8.1. Quay lại GUI FilmAI**

#### **8.2. Chọn workflow:**

```
┌────────────────────────────────────┐
│  Workflow Options:                │
│                                    │
│  ● Full Workflow (All 5 Steps)    │ ← Chọn này
│  ○ Start from Step 2 (Chapters)   │
│  ○ Start from Step 3 (Scenes)     │
│  ○ Start from Step 4 (Prompts)    │
│  ○ Start from Step 5 (Translate)  │
│                                    │
└────────────────────────────────────┘
```

#### **8.3. Click "🚀 Bắt đầu Generate"**

#### **8.4. Theo dõi Log:**

```
┌─ 📋 Tiến trình chạy ────────────────┐
│                                     │
│ ✅ License hợp lệ - Tool đã kích hoạt│
│ 🔑 Đã nạp 3 API key.               │
│ 🔑 Đang dùng API key #1            │
│                                     │
│ ⏳ Đang xử lý...                    │
│                                     │
│ 📝 BƯỚC 1: Generating Chapters     │
│    World Type: medieval             │
│    Model: gemini-2.5-flash         │
│    API Keys: 3 keys                │
│    → Đang tạo chapter 1/6...       │
│    → Đang tạo chapter 2/6...       │
│    ...                              │
│ ✅ Bước 1 hoàn thành!              │
│                                     │
│ 📝 BƯỚC 2: Generating Scenes       │
│    Target scenes: 40                │
│    → Đang tạo scene 1/40...        │
│    → Đang tạo scene 2/40...        │
│    ...                              │
│ ✅ Bước 2 hoàn thành!              │
│                                     │
│ 📝 BƯỚC 3: Generating Prompts      │
│    → Scene 1/40...                 │
│    → Scene 2/40...                 │
│    ...                              │
│ ✅ Bước 3 hoàn thành!              │
│                                     │
│ 📝 BƯỚC 4: Postprocessing          │
│    → Chuẩn hóa JSON...             │
│ ✅ Bước 4 hoàn thành!              │
│                                     │
│ 🌐 BƯỚC 5: Translating to VI       │
│    → Prompt 1/40...                │
│    → Prompt 2/40...                │
│    ...                              │
│ ✅ Bước 5 hoàn thành!              │
│                                     │
│ 🎉 HOÀN TẤT TẤT CẢ!               │
│                                     │
│ 📁 Saved: C:\...\chapters.txt      │
│ 📁 Saved: C:\...\scenes.txt        │
│ 📁 Saved: C:\...\output_prompts... │
│ 📁 Saved: C:\...\final_prompts_en..│
│ 📁 Saved: C:\...\final_prompts_vi..│
│                                     │
└─────────────────────────────────────┘
```

#### **8.5. Thời gian chạy:**

| Số Scenes | Thời gian ước tính |
|-----------|-------------------|
| 12 scenes | ~5-10 phút |
| 40 scenes | ~20-30 phút |
| 60 scenes | ~30-45 phút |
| 100 scenes | ~60-90 phút |

**→ Đợi và theo dõi log!**

---

### **BƯỚC 9: XEM KẾT QUẢ**

#### **9.1. Click "📁 Mở thư mục Output"**

Hoặc vào thư mục XE-CUA-2 thủ công.

#### **9.2. Files được tạo:**

```
📁 XE-CUA-2/
│
├── 📝 chapters.txt                     (6 chapters)
│   Chapter 1: The Fallen Kingdom
│   Chapter 2: The Mentor Appears
│   ...
│
├── 📝 scenes.txt                       (40 scenes)
│   Scene 1: Lana stands on ruins...
│   Scene 2: Adai approaches...
│   ...
│
├── 📝 output_prompts.txt               (JSON thô)
│   {"scene_number":1,...}
│   {"scene_number":2,...}
│   ...
│
├── 📝 output_prompts_clean.txt         (JSON chuẩn)
│   {"scene_number":1,...}  ← Đã chuẩn hóa
│   ...
│
├── 📝 final_prompts_en.txt             ⭐ DÙNG CHO AI VIDEO
│   {"scene_number":1,"scene_title":"The Fallen Kingdom",...}
│   ...
│
└── 📝 final_prompts_vi.txt             ⭐ DÙNG PHỤ ĐỀ/VOICE
    {"scene_number":1,"scene_title":"Vương Quốc Sụp Đổ",...}
    ...
```

---

## 🎥 PHẦN 4: SỬ DỤNG KẾT QUẢ

### **BƯỚC 10: DÙNG PROMPTS CHO AI VIDEO**

#### **10.1. Mở file `final_prompts_en.txt`**

#### **10.2. Copy từng JSON:**

Mỗi dòng là 1 scene:

```json
{"scene_number":1,"scene_title":"The Fallen Kingdom","character":{"name":"Lana","emotions":{"primary":"grief","secondary":"determination"},"voice_tone":"Somber yet resolute"},"setting":{"location":"Ruined castle courtyard","environment":"Debris scattered, broken walls, evening light","time":"Sunset"},"cinematic":{"camera":"Slow tracking shot circling Lana","shot_type":"medium","focus_characters":["Lana"],"lighting":"Golden sunset creating long shadows","mood":"Melancholic yet hopeful","style":"Cinematic 8K realistic","effects":"Dust particles in light beams","sound":"Wind whistling through ruins"},"dialogue":{"characters":[{"speaker":"Lana","line":"This was once my home... I will reclaim it."}]},"action_block":{"length":"150-200 words","content":"Lana stands among the ruins of her kingdom's castle..."}}
```

#### **10.3. Paste vào AI Video tools:**

**VEO (Google):**
```
1. Vào: https://labs.google/veo
2. Paste JSON vào prompt box
3. Generate video
```

**Sora (OpenAI):**
```
1. Vào: https://sora.com
2. Paste JSON
3. Generate
```

**Runway ML:**
```
1. Vào: https://runwayml.com
2. Text to Video
3. Paste JSON
4. Generate
```

**Dreamina:**
```
1. Vào app Dreamina
2. Paste prompt
3. Generate
```

#### **10.4. Dùng file VI cho phụ đề:**

**File:** `final_prompts_vi.txt`

```json
{"scene_number":1,"scene_title":"Vương Quốc Sụp Đổ","character":{"name":"Lana","emotions":{"primary":"đau buồn","secondary":"quyết tâm"},"voice_tone":"Buồn bã nhưng kiên định"},...}
```

**Dùng để:**
- Tạo phụ đề tiếng Việt
- Text-to-Speech tiếng Việt
- Script cho voice actors

---

## 🔧 TROUBLESHOOTING

### **LỖI THƯỜNG GẶP**

#### **1. Lỗi: "Python is not recognized..."**

**Nguyên nhân:** Python chưa được thêm vào PATH

**Cách sửa:**
```
1. Gỡ cài Python
2. Cài lại Python
3. ⚠️ QUAN TRỌNG: Tick ☑️ "Add Python to PATH"
4. Restart Command Prompt
```

#### **2. Lỗi: "No module named 'google.generativeai'"**

**Cách sửa:**
```cmd
pip install google-generativeai
```

#### **3. Lỗi: "Chưa có API keys"**

**Cách sửa:**
```
1. Click Settings
2. Tab API Keys
3. Paste keys
4. Click Lưu
```

#### **4. Lỗi: "story_idea.txt not found"**

**Cách sửa:**
```
1. Tạo file story_idea.txt trong thư mục XE-CUA-2
2. Copy nội dung mẫu ở trên
3. Lưu file
```

#### **5. Lỗi: "Invalid API key"**

**Cách sửa:**
```
1. Vào: https://aistudio.google.com/apikey
2. Kiểm tra key còn hoạt động không
3. Tạo key mới nếu cần
4. Paste lại vào Settings
```

#### **6. App không mở được (double-click không chạy)**

**Cách sửa:**
```
1. Mở Command Prompt
2. cd đến thư mục XE-CUA-2
3. Chạy: python gui_app_enhanced.py
4. Xem lỗi gì hiện ra
```

#### **7. Workflow dừng đột ngột**

**Nguyên nhân:** API quota hết

**Cách sửa:**
```
1. Thêm nhiều API keys hơn (5-10 keys)
2. Đợi quota reset (24h)
3. Hoặc chạy từ bước bị dừng
```

#### **8. Kết quả chất lượng kém**

**Cách sửa:**
```
1. Settings → Configuration
2. Chọn model: Gemini 2.0 Flash Exp
3. Viết story_idea.txt chi tiết hơn
4. Chạy lại
```

#### **9. File output không tìm thấy**

**Cách sửa:**
```
1. Click "📁 Mở thư mục Output"
2. Hoặc vào thủ công: thư mục XE-CUA-2
3. Kiểm tra xem workflow có chạy xong không
```

#### **10. License key không hợp lệ**

**Dùng key mẫu:**
```
ABCD-EFGH-IJKL-MNOP
1234-5678-9012-3456
TEST-KEYS-2024-DEMO
PROD-UCTI-ONKE-Y2024
```

---

## 💡 TIPS & BEST PRACTICES

### **1. Optimize Workflow:**

```
Lần đầu:
→ Dùng story ngắn (3 chapters, 12 scenes)
→ Test xem kết quả có ổn không
→ Adjust settings
→ Scale lên production (6-8 chapters, 60 scenes)
```

### **2. API Keys Management:**

```
Khuyến nghị: 5-10 keys
→ Tool tự động xoay vòng
→ Monitor usage: https://aistudio.google.com
→ Free tier: 1500 requests/day/key
```

### **3. Quality Control:**

```
Review sau mỗi bước:
→ Sau Step 1: Đọc chapters.txt
→ Sau Step 2: Đọc scenes.txt
→ Edit nếu cần
→ Chạy tiếp từ bước sau
```

### **4. Save Time:**

```
→ Lưu story_idea.txt templates
→ Reuse characters & worlds
→ Chạy từng bước riêng nếu cần sửa
```

### **5. Organization:**

```
Tạo thư mục cho từng project:
XE-CUA-2/
├── Projects/
│   ├── Project-Lana/
│   │   ├── story_idea.txt
│   │   ├── chapters.txt
│   │   └── outputs/
│   │
│   └── Project-Alex/
│       ├── story_idea.txt
│       └── outputs/
```

---

## 📚 TÀI LIỆU THAM KHẢO

### **Trong thư mục:**

| File | Nội dung |
|------|----------|
| **README_V2.md** | Tài liệu đầy đủ v2.0 |
| **QUICKSTART_V2.md** | Quick start 10 phút |
| **MO-HINH.txt** | Workflow diagram |
| **SUMMARY_V2_UPGRADE.md** | Tổng kết nâng cấp |
| **HUONG_DAN_TAI_VA_SU_DUNG.md** | File này |

### **Online:**

```
GitHub Repository:
https://github.com/khaitrung89/donggoi

Google AI Studio (lấy API keys):
https://aistudio.google.com/apikey

Python Download:
https://www.python.org/downloads/
```

---

## ✅ CHECKLIST HOÀN THÀNH

Sau khi làm theo hướng dẫn, bạn có:

- [ ] Đã tải và giải nén thư mục XE-CUA-2
- [ ] Đã xóa các thư mục không cần thiết
- [ ] Python đã cài đặt (version 3.8+)
- [ ] Dependencies đã cài (google-generativeai)
- [ ] GUI chạy thành công
- [ ] License đã kích hoạt
- [ ] API keys đã nhập và validate
- [ ] File story_idea.txt đã tạo
- [ ] Đã chạy Full Workflow
- [ ] Có files output: chapters, scenes, final_prompts

**Nếu tất cả ✅ → Bạn đã sẵn sàng tạo phim! 🎬**

---

## 📞 HỖ TRỢ

### **Gặp vấn đề không giải quyết được?**

1. Đọc lại phần Troubleshooting
2. Kiểm tra log trong GUI
3. Chạy từ Command Prompt để xem error
4. Check antivirus/firewall có block không

### **Muốn tính năng mới?**

→ Xem file SUMMARY_V2_UPGRADE.md để biết roadmap

---

**🎉 CHÚC BẠN TẠO PHIM THÀNH CÔNG! 🎬✨**

**Version:** 2.0
**Last Updated:** 2025-11-17
**Author:** FilmAI Team
