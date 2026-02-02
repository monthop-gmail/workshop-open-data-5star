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

# บันได 5+1 ขั้น
# การเปิดเผยข้อมูลสาธารณะ
## 5-Star Open Data + AI-Ready

**Workshop สำหรับหน่วยงานภาครัฐ**

---

# วัตถุประสงค์

- เข้าใจ **5-Star Open Data Model** ตามแนวทาง DGA
- รู้จัก **Level 6: AI-Ready** สำหรับยุค AI
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

# 5+1 Star Model

| ระดับ | ลักษณะ | ตัวอย่าง |
|-------|--------|----------|
| ★ | ข้อมูลบนเว็บ | PDF, Word |
| ★★ | ข้อมูลมีโครงสร้าง | Excel |
| ★★★ | รูปแบบเปิด | CSV, JSON |
| ★★★★ | URI + API | REST API |
| ★★★★★ | Linked Data | RDF, SPARQL |
| ★★★★★★ | **AI-Ready** | Parquet, Embeddings |

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

<!-- _class: lead -->
<!-- _backgroundColor: #8e44ad -->
<!-- _color: white -->

# ★★★★★★ Level 6
## AI-Ready Government Data

---

# Level 6: AI-Ready Data

### ลักษณะ
- ข้อมูลสะอาด ผ่าน Validation
- รูปแบบเหมาะกับ ML: **Parquet, JSONL**
- มี **Data Card** อธิบายการใช้งานกับ AI
- Pre-computed **Embeddings** สำหรับ Vector Search

### ตัวอย่าง
```python
# โหลด Parquet สำหรับ ML
import pandas as pd
df = pd.read_parquet("energy_stats.parquet")

# ใช้กับ RAG
from langchain.vectorstores import FAISS
vectorstore = FAISS.load_local("embeddings/")
```

---

# องค์ประกอบ AI-Ready Data

| องค์ประกอบ | รายละเอียด |
|------------|------------|
| **Data Quality** | Clean, Validated, No missing values |
| **ML Formats** | Parquet, JSONL, Arrow |
| **Data Card** | Use cases, Biases, Limitations |
| **Embeddings** | Vector representations for RAG |
| **Schema** | JSON Schema + ML metadata |
| **Examples** | Working code (Pandas, sklearn, LangChain) |

---

# AI Use Cases

### Machine Learning
- Demand Forecasting (พยากรณ์ความต้องการ)
- Anomaly Detection (ตรวจจับความผิดปกติ)
- Classification & Regression

### Generative AI
- **RAG Q&A System** - ตอบคำถามจากข้อมูล
- **LLM Fine-tuning** - ปรับ LLM ให้เข้าใจโดเมน
- **Chatbot** - บริการประชาชน

```python
qa = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())
answer = qa.run("ภูมิภาคไหนใช้ไฟฟ้ามากที่สุด")
```

---

# Level 5 vs Level 6

| หัวข้อ | Level 5 (Linked Data) | Level 6 (AI-Ready) |
|--------|----------------------|-------------------|
| **เป้าหมาย** | เชื่อมโยงข้อมูล | Train/Run AI |
| **Format** | RDF, Turtle | Parquet, JSONL |
| **Query** | SPARQL | SQL, Vector Search |
| **Metadata** | Ontology, URI | Data Cards, Schema |
| **ผู้ใช้** | Data Engineers | ML/AI Engineers |

---

# สรุปเปรียบเทียบ 6 ระดับ

| ระดับ | รูปแบบ | Machine | Real-time | Linkable | AI-Ready |
|-------|--------|---------|-----------|----------|----------|
| ★ | PDF | ❌ | ❌ | ❌ | ❌ |
| ★★ | Excel | ✅ | ❌ | ❌ | ❌ |
| ★★★ | JSON | ✅ | ❌ | ❌ | ❌ |
| ★★★★ | API | ✅ | ✅ | ❌ | ❌ |
| ★★★★★ | RDF | ✅ | ✅ | ✅ | ❌ |
| ★★★★★★ | Parquet | ✅ | ✅ | ✅ | ✅ |

---

# Roadmap การยกระดับข้อมูล

```
ปัจจุบัน    ระยะสั้น     ระยะกลาง    ระยะยาว     อนาคต
   │           │            │           │           │
   ▼           ▼            ▼           ▼           ▼
┌─────┐    ┌─────┐      ┌─────┐     ┌─────┐    ┌──────┐
│  ★  │ ─► │ ★★★ │ ───► │★★★★ │ ──► │★★★★★│ ─► │★★★★★★│
│ PDF │    │JSON │      │ API │     │ RDF │    │  AI  │
└─────┘    └─────┘      └─────┘     └─────┘    └──────┘
```

### แนะนำ
- เริ่มจาก Level 3 (JSON/CSV with metadata)
- พัฒนา API (Level 4) สำหรับ real-time
- **Level 6 (AI-Ready)** สำหรับข้อมูลที่จะใช้กับ AI

---

<!-- _class: lead -->
<!-- _backgroundColor: #1a5f7a -->
<!-- _color: white -->

# Hands-on Workshop
## ลงมือปฏิบัติ

---

# แบบฝึกหัด

| # | หัวข้อ | รายละเอียด |
|---|--------|------------|
| 1 | Level 1 → 2 | แปลงข้อมูลจาก Markdown เป็น CSV |
| 2 | Level 2 → 3 | เพิ่ม metadata ให้ CSV กลายเป็น JSON |
| 3 | Level 3 → 4 | รัน API server และลองเรียก API |
| 4 | Level 4 → 5 | Query ข้อมูล RDF ด้วย SPARQL |
| 5 | Level 5 → 6 | สร้าง Parquet และ RAG Q&A |

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
- Google Data Cards
- HuggingFace Dataset Documentation

---

<!-- _class: lead -->
<!-- _backgroundColor: #1a5f7a -->
<!-- _color: white -->

# ขอบคุณครับ
## Q&A

**Workshop: 5+1 Star Open Data (AI-Ready)**
