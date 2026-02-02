# Workshop: บันได 5 ขั้นการเปิดเผยข้อมูลสาธารณะ (5-Star Open Data)

## ภาพรวม

Workshop นี้ใช้ข้อมูลชุดเดียวกัน **"สถิติการใช้พลังงานไฟฟ้าตามภูมิภาค ปี 2566"**
แสดงในรูปแบบต่างๆ ตามระดับความเปิดของข้อมูล

```
workshop-data/
├── level1_basic/           ★ ข้อมูลพื้นฐาน
├── level2_structured/      ★★ ข้อมูลมีโครงสร้าง
├── level3_open_format/     ★★★ รูปแบบเปิด
├── level4_api/             ★★★★ เปิดผ่าน API
└── level5_linked_data/     ★★★★★ Linked Open Data
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

**ไฟล์:** `level3_open_format/energy_stats_2566.json`

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

## สรุปเปรียบเทียบ

| ระดับ | รูปแบบ | Machine-Readable | Real-time | Linkable |
|-------|--------|------------------|-----------|----------|
| ★ | PDF, Word | ❌ | ❌ | ❌ |
| ★★ | Excel, CSV | ✅ | ❌ | ❌ |
| ★★★ | JSON, XML | ✅ | ❌ | ❌ |
| ★★★★ | REST API | ✅ | ✅ | ❌ |
| ★★★★★ | RDF, SPARQL | ✅ | ✅ | ✅ |

---

## แบบฝึกหัด

1. **Level 1 → 2:** แปลงข้อมูลจาก `energy_report_2566.md` เป็น CSV ด้วยมือ
2. **Level 2 → 3:** เพิ่ม metadata ลงใน CSV ให้กลายเป็น JSON ที่สมบูรณ์
3. **Level 3 → 4:** รัน API server และลองเรียก API ด้วย curl หรือ Python
4. **Level 4 → 5:** ลอง query ข้อมูล RDF ด้วย SPARQL (ใช้ Apache Jena หรือ online SPARQL playground)

---

*จัดทำสำหรับ Workshop: Open Data 5-Star Model*
