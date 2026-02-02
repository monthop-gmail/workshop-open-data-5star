# Slides: Workshop 5-Star Open Data

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

## เนื้อหา Slides

1. Open Data คืออะไร
2. 5-Star Model Overview
3. Level 1: Basic (PDF, Word)
4. Level 2: Structured (Excel, CSV)
5. Level 3: Open Format (JSON, XML)
6. Level 4: API
7. Level 5: Linked Data (RDF)
8. สรุปเปรียบเทียบ
9. Roadmap การยกระดับ
10. Hands-on Workshop
