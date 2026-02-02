---
marp: true
theme: default
paginate: true
backgroundColor: #fff
style: |
  section {
    font-family: 'Sarabun', 'Noto Sans Thai', sans-serif;
  }
  h1 {
    color: #1a5f7a;
  }
  h2 {
    color: #2c3e50;
  }
  table {
    font-size: 0.8em;
  }
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
---

<!-- _class: lead -->
<!-- _backgroundColor: #1a5f7a -->
<!-- _color: white -->

# บันได 5 ขั้น
# การเปิดเผยข้อมูลสาธารณะ
## 5-Star Open Data Model

**Workshop สำหรับหน่วยงานภาครัฐ**

---

# วัตถุประสงค์

- เข้าใจ **5-Star Open Data Model** ตามแนวทาง DGA
- เห็นความแตกต่างของแต่ละระดับ
- ลงมือปฏิบัติจริงกับข้อมูลตัวอย่าง
- วางแผนยกระดับข้อมูลของหน่วยงาน

---

# Open Data คืออะไร?

> ข้อมูลที่ **ใครก็ได้** สามารถ **เข้าถึง ใช้งาน และแบ่งปัน** ได้อย่างเสรี

### องค์ประกอบสำคัญ

| หัวข้อ | คำอธิบาย |
|--------|----------|
| **Available** | เข้าถึงได้ผ่านอินเทอร์เน็ต |
| **Machine-readable** | คอมพิวเตอร์อ่านและประมวลผลได้ |
| **Open Format** | ไม่ผูกกับซอฟต์แวร์เฉพาะ |
| **Open License** | อนุญาตให้นำไปใช้ต่อได้ |

---

# 5-Star Model โดย Tim Berners-Lee

![bg right:40% 80%](https://5stardata.info/images/5-star-steps.png)

| ระดับ | ลักษณะ |
|-------|--------|
| ★ | ข้อมูลบนเว็บ (รูปแบบใดก็ได้) |
| ★★ | ข้อมูลมีโครงสร้าง (Excel) |
| ★★★ | รูปแบบเปิด (CSV, JSON) |
| ★★★★ | ใช้ URI ระบุตัวตน + API |
| ★★★★★ | เชื่อมโยงข้อมูลอื่น (Linked Data) |

---

<!-- _class: lead -->
<!-- _backgroundColor: #e74c3c -->
<!-- _color: white -->

# ★ Level 1
## ข้อมูลพื้นฐาน (Basic)

---

# Level 1: ข้อมูลพื้นฐาน

### รูปแบบ
- PDF, Word, รูปภาพ, สแกนเอกสาร

### ตัวอย่าง
```
รายงานสถิติการใช้พลังงานไฟฟ้า ปี 2566

ภาคกลาง: 45,230 ล้านหน่วย
ภาคเหนือ: 18,450 ล้านหน่วย
ภาคอีสาน: 22,180 ล้านหน่วย
...
```

### ข้อจำกัด
❌ Copy-paste หรือพิมพ์ใหม่ | ❌ ไม่สามารถคำนวณอัตโนมัติ

---

<!-- _class: lead -->
<!-- _backgroundColor: #e67e22 -->
<!-- _color: white -->

# ★★ Level 2
## ข้อมูลมีโครงสร้าง (Structured)

---

# Level 2: ข้อมูลมีโครงสร้าง

### รูปแบบ
- Excel (.xlsx), CSV

### ตัวอย่าง
```csv
region_th,region_en,consumption_gwh,customers,growth_rate
ภาคกลาง,Central,45230,8542000,3.2
ภาคเหนือ,North,18450,4125000,2.8
ภาคอีสาน,Northeast,22180,7890000,4.1
```

### ข้อดี
✅ Import เข้า Excel/Python ได้ | ✅ คำนวณต่อได้

### ข้อจำกัด
❌ ยังผูกกับ proprietary format | ❌ ไม่มี metadata

---

<!-- _class: lead -->
<!-- _backgroundColor: #f39c12 -->
<!-- _color: white -->

# ★★★ Level 3
## รูปแบบเปิด (Open Format)

---

# Level 3: รูปแบบเปิด

### รูปแบบ
- JSON, XML, CSV (with metadata)

### ตัวอย่าง JSON
```json
{
  "metadata": {
    "source": "กรมพัฒนาพลังงานทดแทนฯ",
    "license": "Open Government License"
  },
  "data": [
    {"region": "ภาคกลาง", "consumption_gwh": 45230}
  ]
}
```

### ข้อดี
✅ ไม่ผูกซอฟต์แวร์ | ✅ มี metadata | ✅ ระบุ license ชัดเจน

---

# JSON vs XML

| หัวข้อ | JSON | XML |
|--------|------|-----|
| ขนาดไฟล์ | เล็กกว่า | ใหญ่กว่า |
| อ่านง่าย | ✅ | ปานกลาง |
| หลายภาษา | แยก field | ใช้ `lang` attribute |
| Validation | JSON Schema | XSD |
| เหมาะกับ | Web API | Enterprise |

---

<!-- _class: lead -->
<!-- _backgroundColor: #27ae60 -->
<!-- _color: white -->

# ★★★★ Level 4
## เปิดผ่าน API

---

# Level 4: Open with API

### ลักษณะ
- REST API / GraphQL
- มี endpoint ให้เรียกข้อมูล

### ตัวอย่าง
```bash
# ดึงข้อมูลภาคอีสาน
curl https://api.example.go.th/energy/regions/TH-NE

# Response
{
  "region": "ภาคตะวันออกเฉียงเหนือ",
  "consumption_gwh": 22180,
  "growth_rate": 4.1
}
```

---

# ข้อดีของ API

| ข้อดี | คำอธิบาย |
|-------|----------|
| **Real-time** | ข้อมูลอัปเดตตลอด ไม่ต้องดาวน์โหลดซ้ำ |
| **Selective** | เลือกดึงเฉพาะข้อมูลที่ต้องการ |
| **Integrate** | เชื่อมต่อกับแอปอื่นอัตโนมัติ |
| **Scalable** | รองรับผู้ใช้จำนวนมาก |

### ตัวอย่าง API ภาครัฐไทย
- กรมอุตุนิยมวิทยา
- ขสมก. (ตำแหน่งรถเมล์)
- data.go.th

---

<!-- _class: lead -->
<!-- _backgroundColor: #2980b9 -->
<!-- _color: white -->

# ★★★★★ Level 5
## Linked Open Data

---

# Level 5: Linked Open Data

### ลักษณะ
- ใช้ RDF (Resource Description Framework)
- มี URI ระบุตัวตนข้อมูล
- เชื่อมโยงกับข้อมูลภายนอก (DBpedia, Wikidata)

### ตัวอย่าง RDF (Turtle)
```turtle
stat:northeast
    energy:region region:TH-NE ;
    energy:consumptionGWh "22180" ;
    owl:sameAs dbr:Isan .  # เชื่อมกับ DBpedia
```

---

# ประโยชน์ของ Linked Data

### Knowledge Graph
```
[สถิติพลังงาน] ──> [ภาคอีสาน] ──> [DBpedia:Isan]
                         │
                         └──> [จังหวัด] ──> [Wikidata]
```

### ข้อดี
✅ เชื่อมโยงข้อมูลข้ามหน่วยงาน
✅ Query ด้วย SPARQL
✅ สร้าง Knowledge Graph ได้
✅ Semantic Web ready

---

# สรุปเปรียบเทียบ 5 ระดับ

| ระดับ | รูปแบบ | Machine | Real-time | Linkable |
|-------|--------|---------|-----------|----------|
| ★ | PDF | ❌ | ❌ | ❌ |
| ★★ | Excel | ✅ | ❌ | ❌ |
| ★★★ | JSON/XML | ✅ | ❌ | ❌ |
| ★★★★ | API | ✅ | ✅ | ❌ |
| ★★★★★ | RDF | ✅ | ✅ | ✅ |

---

# Roadmap การยกระดับข้อมูล

```
ปัจจุบัน        ระยะสั้น         ระยะกลาง        ระยะยาว
   │               │                │               │
   ▼               ▼                ▼               ▼
┌──────┐      ┌──────┐         ┌──────┐       ┌──────┐
│  ★   │ ───► │ ★★★  │ ──────► │ ★★★★ │ ────► │★★★★★│
│ PDF  │      │ JSON │         │ API  │       │ RDF  │
└──────┘      └──────┘         └──────┘       └──────┘
```

### แนะนำ
- เริ่มจาก Level 3 (JSON/CSV with metadata)
- ค่อยๆ พัฒนา API (Level 4)
- Linked Data สำหรับข้อมูลสำคัญ

---

<!-- _class: lead -->
<!-- _backgroundColor: #1a5f7a -->
<!-- _color: white -->

# Hands-on Workshop
## ลงมือปฏิบัติ

---

# แบบฝึกหัด

### Exercise 1: Level 1 → 2
แปลงข้อมูลจากรายงาน Markdown เป็น CSV

### Exercise 2: Level 2 → 3
เพิ่ม metadata ให้ CSV กลายเป็น JSON ที่สมบูรณ์

### Exercise 3: Level 3 → 4
รัน API server และลองเรียก API

### Exercise 4: Level 4 → 5
ลอง query ข้อมูล RDF ด้วย SPARQL

---

# Resources

### ไฟล์ตัวอย่าง
```
github.com/monthop-gmail/workshop-open-data-5star
```

### อ้างอิง
- 5stardata.info
- data.go.th
- DGA แนวทางการเปิดเผยข้อมูลสาธารณะ

---

<!-- _class: lead -->
<!-- _backgroundColor: #1a5f7a -->
<!-- _color: white -->

# ขอบคุณครับ
## Q&A

**Workshop: 5-Star Open Data**
