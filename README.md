# Workshop: บันได 5+1 ขั้นการเปิดเผยข้อมูลสาธารณะ (5-Star + AI-Ready)

## ภาพรวม

Workshop นี้ใช้ข้อมูลชุดเดียวกัน **"สถิติการใช้พลังงานไฟฟ้าตามภูมิภาค ปี 2566"**
แสดงในรูปแบบต่างๆ ตามระดับความเปิดของข้อมูล รวมถึง **Level 6: AI-Ready** สำหรับยุค AI

```
workshop-data/
├── level1_basic/           ★ ข้อมูลพื้นฐาน
├── level2_structured/      ★★ ข้อมูลมีโครงสร้าง
├── level3_open_format/     ★★★ รูปแบบเปิด
├── level4_api/             ★★★★ เปิดผ่าน API
├── level5_linked_data/     ★★★★★ Linked Open Data
├── level6_ai_ready/        ★★★★★★ AI-Ready Data
├── docker/                 🐳 Docker Compose
└── slides/                 📊 Presentation
```

---

## ★ Level 1: ข้อมูลพื้นฐาน (Basic)

**ไฟล์:** `level1_basic/energy_report_2566.md`

### ลักษณะ
- ข้อมูลอยู่ในรูปเอกสาร (PDF, Word, Markdown)
- อ่านได้ด้วยคน แต่ machine-readable ไม่ดี
- ต้อง copy-paste หรือพิมพ์ใหม่เพื่อนำไปใช้

### ข้อจำกัด
```
❌ ไม่สามารถนำไปคำนวณได้โดยตรง
❌ ต้องแปลงข้อมูลด้วยมือ
❌ โครงสร้างไม่ชัดเจน
```

---

## ★★ Level 2: ข้อมูลมีโครงสร้าง (Structured)

**ไฟล์:** `level2_structured/energy_stats_2566.csv`

### ลักษณะ
- ข้อมูลอยู่ในรูปตาราง (Excel, CSV)
- มี header ระบุชื่อคอลัมน์
- นำไปคำนวณต่อได้

### ตัวอย่างการใช้งาน
```python
import pandas as pd
df = pd.read_csv('energy_stats_2566.csv')
print(df['consumption_gwh'].sum())  # รวมการใช้ไฟฟ้า
```

### ข้อจำกัด
```
❌ ยังผูกกับ proprietary format (Excel)
❌ ไม่มี metadata อธิบายข้อมูล
❌ ต้องดาวน์โหลดไฟล์ทั้งหมด
```

---

## ★★★ Level 3: รูปแบบเปิด (Open Format)

**ไฟล์:**
- `level3_open_format/energy_stats_2566.json`
- `level3_open_format/energy_stats_2566.xml`

### ลักษณะ
- ใช้รูปแบบมาตรฐานเปิด (JSON, XML, CSV)
- มี metadata อธิบายข้อมูล
- ไม่ต้องใช้ซอฟต์แวร์ proprietary

### ตัวอย่างการใช้งาน
```python
import json
with open('energy_stats_2566.json') as f:
    data = json.load(f)

print(f"แหล่งข้อมูล: {data['metadata']['source']}")
print(f"สัญญาอนุญาต: {data['metadata']['license']}")

for region in data['data']:
    print(f"{region['region_th']}: {region['consumption_gwh']:,} GWh")
```

### ข้อดี
```
✅ ใช้งานได้กับซอฟต์แวร์หลากหลาย
✅ มี metadata ครบถ้วน
✅ ระบุ license ชัดเจน
```

---

## ★★★★ Level 4: เปิดผ่าน API (Open with API)

**ไฟล์:**
- `level4_api/api_server.py` - ตัว API server
- `level4_api/api_client_example.py` - ตัวอย่างการเรียก API
- `level4_api/curl_examples.sh` - ตัวอย่าง curl

### การรัน API Server
```bash
cd level4_api
pip install flask flask-cors
python api_server.py
```

### API Endpoints
| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/energy/regions` | ดึงข้อมูลทุกภูมิภาค |
| `GET /api/v1/energy/regions/{code}` | ดึงข้อมูลภูมิภาคเดียว |
| `GET /api/v1/energy/summary` | ดึงข้อมูลสรุป |

### ตัวอย่างการเรียก API
```bash
# ดึงข้อมูลภาคอีสาน
curl http://localhost:5000/api/v1/energy/regions/TH-NE

# ดึงข้อมูลสรุป
curl http://localhost:5000/api/v1/energy/summary
```

### ข้อดี
```
✅ เข้าถึงข้อมูลแบบ real-time
✅ เลือกดึงเฉพาะข้อมูลที่ต้องการ
✅ เชื่อมต่อกับแอปพลิเคชันอื่นได้อัตโนมัติ
✅ ข้อมูลอัปเดตตลอดเวลา
```

---

## ★★★★★ Level 5: Linked Open Data

**ไฟล์:**
- `level5_linked_data/energy_stats_2566.ttl` - ข้อมูล RDF (Turtle format)
- `level5_linked_data/sparql_examples.rq` - ตัวอย่าง SPARQL queries

### ลักษณะ
- ใช้ RDF (Resource Description Framework)
- มี URI ระบุตัวตนของข้อมูล
- เชื่อมโยงกับข้อมูลภายนอก (เช่น DBpedia, Wikidata)
- รองรับ Semantic Web

### ตัวอย่าง RDF (Turtle)
```turtle
stat:northeast
    a energy:EnergyConsumptionStat ;
    energy:region region:TH-NE ;
    energy:consumptionGWh "22180"^^xsd:decimal ;
    energy:numberOfCustomers "7890000"^^xsd:integer .

region:TH-NE
    rdfs:label "ภาคตะวันออกเฉียงเหนือ"@th ;
    owl:sameAs dbr:Isan ;     # เชื่อมโยงกับ DBpedia
    dbo:country dbr:Thailand .
```

### ตัวอย่าง SPARQL Query
```sparql
PREFIX energy: <http://data.go.th/def/energy/>

SELECT ?regionName ?consumption
WHERE {
    ?stat energy:region ?region ;
          energy:consumptionGWh ?consumption .
    ?region rdfs:label ?regionName .
    FILTER (lang(?regionName) = "th")
}
ORDER BY DESC(?consumption)
```

### ข้อดี
```
✅ เชื่อมโยงข้อมูลข้ามแหล่ง (Cross-dataset linking)
✅ มี URI อ้างอิงได้ทั่วโลก
✅ รองรับ Semantic queries
✅ สร้าง Knowledge Graph ได้
```

---

## ★★★★★★ Level 6: AI-Ready Government Data

**ไฟล์:**
- `level6_ai_ready/datacard.md` - Data Card สำหรับ AI
- `level6_ai_ready/schema.json` - JSON Schema + ML metadata
- `level6_ai_ready/validation.py` - ตรวจสอบคุณภาพข้อมูล
- `level6_ai_ready/prepare_data.py` - สร้าง Parquet/Embeddings
- `level6_ai_ready/data/` - ข้อมูลในรูปแบบ AI-Ready
- `level6_ai_ready/examples/` - ตัวอย่างการใช้งาน

### ลักษณะ
- ข้อมูลสะอาด ผ่าน Validation
- รูปแบบเหมาะกับ ML: Parquet, JSONL
- มี Data Card อธิบายการใช้งานกับ AI
- Pre-computed Embeddings สำหรับ Vector Search
- ตัวอย่างโค้ดพร้อมใช้งาน

### AI-Ready Formats
| Format | File | Use Case |
|--------|------|----------|
| JSONL | `energy_stats.jsonl` | LLM fine-tuning |
| CSV | `energy_stats_clean.csv` | General ML |
| Parquet | `energy_stats.parquet` | Big data (generated) |
| Embeddings | `embeddings.json` | Vector search (generated) |

### ตัวอย่างการใช้งาน

#### Data Analysis
```python
import pandas as pd
df = pd.read_parquet("data/energy_stats.parquet")
print(df.describe())
```

#### Machine Learning
```python
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(X_train, y_train)
```

#### RAG Q&A
```python
from langchain.chains import RetrievalQA
qa = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())
answer = qa.run("ภูมิภาคไหนใช้ไฟฟ้ามากที่สุด")
```

### Quick Start
```bash
cd level6_ai_ready

# 1. Validate data
python validation.py

# 2. Prepare AI-ready formats
pip install pandas pyarrow sentence-transformers
python prepare_data.py

# 3. Run examples
python examples/pandas_analysis.py
python examples/sklearn_example.py
python examples/langchain_rag.py
```

### ข้อดี
```
✅ พร้อมใช้กับ AI/ML ทันที
✅ มี Data Card อธิบาย use cases และ limitations
✅ Validated data quality
✅ Pre-computed embeddings สำหรับ RAG
✅ Working code examples
```

---

## 🐳 Docker Compose

รัน API + SPARQL endpoint ด้วย Docker:

```bash
cd docker
docker-compose up -d
```

### Services
| Service | Port | Description |
|---------|------|-------------|
| web | 8080 | Web UI + Slides |
| api | 5000 | REST API (Level 4) |
| fuseki | 3030 | SPARQL (Level 5) |

---

## 📊 Slides

เปิด slides ได้ที่ `slides/index.html` หรือ:

```bash
# ด้วย Live Server
npx serve slides/

# Export เป็น PDF (Marp)
npm install -g @marp-team/marp-cli
marp slides/presentation.md -o presentation.pdf
```

---

## สรุปเปรียบเทียบ

| ระดับ | รูปแบบ | Machine | Real-time | Linkable | AI-Ready |
|-------|--------|---------|-----------|----------|----------|
| ★ | PDF, Word | ❌ | ❌ | ❌ | ❌ |
| ★★ | Excel, CSV | ✅ | ❌ | ❌ | ❌ |
| ★★★ | JSON, XML | ✅ | ❌ | ❌ | ❌ |
| ★★★★ | REST API | ✅ | ✅ | ❌ | ❌ |
| ★★★★★ | RDF, SPARQL | ✅ | ✅ | ✅ | ❌ |
| ★★★★★★ | Parquet, Embeddings | ✅ | ✅ | ✅ | ✅ |

---

## แบบฝึกหัด

| # | หัวข้อ | รายละเอียด |
|---|--------|------------|
| 1 | Level 1 → 2 | แปลงข้อมูลจาก Markdown เป็น CSV |
| 2 | Level 2 → 3 | เพิ่ม metadata ให้ CSV กลายเป็น JSON |
| 3 | Level 3 → 4 | รัน API server และลองเรียก API |
| 4 | Level 4 → 5 | Query ข้อมูล RDF ด้วย SPARQL |
| 5 | Level 5 → 6 | สร้าง Parquet และ RAG Q&A |

---

## Roadmap การยกระดับข้อมูล

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
- พัฒนา API (Level 4) สำหรับ real-time access
- Level 6 (AI-Ready) สำหรับข้อมูลที่จะใช้กับ AI

---

*จัดทำสำหรับ Workshop: 5+1 Star Open Data Model (AI-Ready)*
