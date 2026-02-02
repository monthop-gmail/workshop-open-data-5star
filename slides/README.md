# Slides: Workshop 5+1 Star Open Data (AI-Ready)

## ไฟล์ที่มี

| ไฟล์ | รูปแบบ | วิธีใช้ |
|------|--------|--------|
| `index.html` | Reveal.js | เปิดใน browser ได้เลย |
| `presentation.md` | Marp | Export เป็น PDF/PPTX |

---

## 1. Reveal.js (แนะนำ)

### เปิดใน Browser
```bash
# วิธีง่ายสุด - เปิดไฟล์โดยตรง
open slides/index.html          # macOS
xdg-open slides/index.html      # Linux
start slides/index.html         # Windows

# หรือใช้ Live Server
npx serve slides/
```

### Keyboard Shortcuts
| ปุ่ม | การทำงาน |
|------|----------|
| `→` / `Space` | หน้าถัดไป |
| `←` | หน้าก่อนหน้า |
| `Esc` | ดูภาพรวม |
| `F` | เต็มจอ |
| `S` | Speaker notes |

---

## 2. Marp (Export PDF/PPTX)

### ติดตั้ง Marp CLI
```bash
npm install -g @marp-team/marp-cli
```

### Export เป็น PDF
```bash
marp presentation.md -o presentation.pdf
```

### Export เป็น PPTX
```bash
marp presentation.md -o presentation.pptx
```

### Export เป็น HTML
```bash
marp presentation.md -o presentation-marp.html
```

### ใช้กับ VS Code
1. ติดตั้ง extension "Marp for VS Code"
2. เปิด `presentation.md`
3. กด Preview หรือ Export

---

## เนื้อหา Slides (27 หน้า)

| # | หัวข้อ | สี |
|---|--------|-----|
| 1-2 | Title & วัตถุประสงค์ | น้ำเงิน |
| 3-4 | Open Data & 5+1 Star Overview | ขาว |
| 5-6 | ★ Level 1: Basic | แดง |
| 7-8 | ★★ Level 2: Structured | ส้ม |
| 9-11 | ★★★ Level 3: Open Format + JSON vs XML | เหลือง |
| 12-14 | ★★★★ Level 4: API | เขียว |
| 15-17 | ★★★★★ Level 5: Linked Data | น้ำเงิน |
| 18-22 | ★★★★★★ **Level 6: AI-Ready** | ม่วง |
| 23-24 | สรุปเปรียบเทียบ 6 ระดับ & Roadmap | ขาว |
| 25-27 | Workshop & Resources & Q&A | น้ำเงิน |

---

## Level 6: AI-Ready (ใหม่)

Slides สำหรับ Level 6 ประกอบด้วย:

1. **AI-Ready Data Overview**
   - ลักษณะข้อมูล AI-Ready
   - ตัวอย่างโค้ด Python

2. **องค์ประกอบ AI-Ready Data**
   - Data Quality
   - ML Formats (Parquet, JSONL)
   - Data Card
   - Embeddings
   - Schema
   - Examples

3. **AI Use Cases**
   - Machine Learning (Forecasting, Anomaly Detection)
   - Generative AI (RAG, Fine-tuning, Chatbot)

4. **Level 5 vs Level 6 Comparison**
   - เป้าหมาย, Format, Query, Metadata, ผู้ใช้

---

## สีประจำแต่ละ Level

| Level | สี | Hex Code |
|-------|-----|----------|
| ★ Level 1 | แดง | `#e74c3c` |
| ★★ Level 2 | ส้ม | `#e67e22` |
| ★★★ Level 3 | เหลือง | `#f39c12` |
| ★★★★ Level 4 | เขียว | `#27ae60` |
| ★★★★★ Level 5 | น้ำเงิน | `#2980b9` |
| ★★★★★★ Level 6 | ม่วง | `#8e44ad` |

---

## ตัวอย่างการใช้งาน

### Workshop แบบเต็ม (3 ชั่วโมง)
- ใช้ทุก slides
- ทำ hands-on ทุก exercise

### Workshop แบบย่อ (1.5 ชั่วโมง)
- ข้าม JSON vs XML
- ข้าม Level 5 vs Level 6 comparison
- เลือก exercise 2-3 ข้อ

### Focus AI-Ready (1 ชั่วโมง)
- Overview → Level 6 → Use Cases → Workshop
- เหมาะสำหรับผู้ที่รู้ 5-Star แล้ว
