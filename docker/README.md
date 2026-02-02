# Docker Setup: 5+1 Star Open Data Workshop (AI-Ready)

## Services

| Service | Port | Level | Description |
|---------|------|-------|-------------|
| **web** | 8080 | - | Web UI + Slides |
| **api** | 5000 | ★★★★ | REST API (Level 4) |
| **fuseki** | 3030 | ★★★★★ | SPARQL Endpoint (Level 5) |

> **Level 6 (AI-Ready):** ใช้ไฟล์ใน `level6_ai_ready/` โดยตรง ไม่ต้องรัน Docker

## Quick Start

```bash
# รัน services ทั้งหมด
docker-compose up -d

# ดู logs
docker-compose logs -f

# หยุด services
docker-compose down
```

## URLs

| URL | Level | Description |
|-----|-------|-------------|
| http://localhost:8080 | - | Web UI (Demo) |
| http://localhost:8080/slides/ | - | Presentation Slides |
| http://localhost:5000 | ★★★★ | API Documentation |
| http://localhost:5000/api/v1/energy/regions | ★★★★ | API: ข้อมูลทุกภูมิภาค |
| http://localhost:3030 | ★★★★★ | Fuseki Admin UI |
| http://localhost:3030/#/dataset/energy/query | ★★★★★ | SPARQL Query UI |

---

## ★★★★ Level 4: REST API

### Endpoints

```bash
# ข้อมูลทุกภูมิภาค
curl http://localhost:5000/api/v1/energy/regions

# ข้อมูลภาคอีสาน
curl http://localhost:5000/api/v1/energy/regions/TH-NE

# ข้อมูลสรุป
curl http://localhost:5000/api/v1/energy/summary
```

### ผ่าน Web UI
```bash
curl http://localhost:8080/api/v1/energy/regions
```

---

## ★★★★★ Level 5: SPARQL

### Query ผ่าน curl

```bash
# ดึงข้อมูลทุกภูมิภาค
curl -X POST http://localhost:3030/energy/sparql \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: application/json" \
  -d 'query=PREFIX energy: <http://data.go.th/def/energy/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?name ?consumption WHERE { ?stat energy:region ?region ; energy:consumptionGWh ?consumption . ?region rdfs:label ?name . FILTER(lang(?name)="th") }'
```

### Query ผ่าน Fuseki UI

1. เปิด http://localhost:3030
2. Login: admin / admin123
3. เลือก dataset "energy"
4. ไปที่ Query tab
5. ใส่ SPARQL query

### ตัวอย่าง SPARQL Queries

```sparql
# Query 1: ดึงข้อมูลทุกภูมิภาค
PREFIX energy: <http://data.go.th/def/energy/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?regionName ?consumption ?customers ?growth
WHERE {
    ?stat a energy:EnergyConsumptionStat ;
          energy:region ?region ;
          energy:consumptionGWh ?consumption ;
          energy:numberOfCustomers ?customers ;
          energy:growthRate ?growth .
    ?region rdfs:label ?regionName .
    FILTER (lang(?regionName) = "th")
}
ORDER BY DESC(?consumption)
```

```sparql
# Query 2: หาภูมิภาคที่เติบโตสูงสุด
PREFIX energy: <http://data.go.th/def/energy/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?regionName ?growth
WHERE {
    ?stat energy:region ?region ;
          energy:growthRate ?growth .
    ?region rdfs:label ?regionName .
    FILTER (lang(?regionName) = "th")
}
ORDER BY DESC(?growth)
LIMIT 1
```

```sparql
# Query 3: รวมการใช้ไฟฟ้าทั้งประเทศ
PREFIX energy: <http://data.go.th/def/energy/>

SELECT (SUM(?consumption) AS ?total) (SUM(?customers) AS ?totalCustomers)
WHERE {
    ?stat energy:consumptionGWh ?consumption ;
          energy:numberOfCustomers ?customers .
}
```

---

## ★★★★★★ Level 6: AI-Ready

Level 6 ไม่ต้องใช้ Docker แต่ใช้ไฟล์และ Python scripts โดยตรง

### Quick Start

```bash
cd ../level6_ai_ready

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

### ไฟล์ที่สำคัญ

| ไฟล์ | รายละเอียด |
|------|------------|
| `data/energy_stats.jsonl` | JSONL สำหรับ LLM fine-tuning |
| `data/energy_stats.parquet` | Parquet สำหรับ ML (generated) |
| `data/embeddings.json` | Vector embeddings (generated) |
| `datacard.md` | Data Card สำหรับ AI |
| `schema.json` | JSON Schema + ML metadata |

### ใช้ร่วมกับ Docker Services

```python
import requests
import pandas as pd

# ดึงข้อมูลจาก API (Level 4) แล้วแปลงเป็น AI-Ready
response = requests.get("http://localhost:5000/api/v1/energy/regions")
data = response.json()["data"]

# แปลงเป็น DataFrame
df = pd.DataFrame(data)

# Save as Parquet (AI-Ready)
df.to_parquet("energy_from_api.parquet")

# ใช้กับ ML
from sklearn.preprocessing import StandardScaler
X = df[["customers", "growth_rate"]].values
X_scaled = StandardScaler().fit_transform(X)
```

### RAG with API Data

```python
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS

# สร้าง documents จาก API
response = requests.get("http://localhost:5000/api/v1/energy/regions")
regions = response.json()["data"]

documents = []
for r in regions:
    doc = f"{r['region_th']} มีการใช้ไฟฟ้า {r['consumption_gwh']:,} GWh"
    documents.append(doc)

# สร้าง vector store และใช้ RAG
# ... (ดูตัวอย่างเต็มใน level6_ai_ready/examples/langchain_rag.py)
```

---

## Troubleshooting

### ตรวจสอบ Services

```bash
# ดู status
docker-compose ps

# ดู logs ของ api
docker-compose logs api

# ดู logs ของ fuseki
docker-compose logs fuseki

# ดู logs ของ data-loader
docker-compose logs data-loader
```

### รีโหลดข้อมูล SPARQL

```bash
# รีรัน data-loader
docker-compose up -d --force-recreate data-loader
```

### Reset ทั้งหมด

```bash
# ลบ volumes และเริ่มใหม่
docker-compose down -v
docker-compose up -d
```

---

## Architecture

```
                    ┌─────────────────┐
                    │   Web Browser   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  nginx (:8080)  │
                    │   - Web UI      │
                    │   - Slides      │
                    │   - Proxy       │
                    └───┬─────────┬───┘
                        │         │
           ┌────────────▼─┐   ┌───▼────────────┐
           │  API (:5000) │   │ Fuseki (:3030) │
           │   ★★★★       │   │    ★★★★★       │
           │  REST API    │   │    SPARQL      │
           └──────────────┘   └───────┬────────┘
                                      │
                              ┌───────▼────────┐
                              │  RDF Data      │
                              │  (Turtle)      │
                              └────────────────┘

    ┌─────────────────────────────────────────────────┐
    │              ★★★★★★ Level 6: AI-Ready           │
    │  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │
    │  │ Parquet │  │  JSONL  │  │   Embeddings    │  │
    │  └─────────┘  └─────────┘  └─────────────────┘  │
    │         │           │              │            │
    │         ▼           ▼              ▼            │
    │  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │
    │  │ Pandas  │  │Fine-tune│  │  RAG / Vector   │  │
    │  │ sklearn │  │   LLM   │  │     Search      │  │
    │  └─────────┘  └─────────┘  └─────────────────┘  │
    └─────────────────────────────────────────────────┘
```

---

## Credentials

| Service | Username | Password |
|---------|----------|----------|
| Fuseki Admin | admin | admin123 |

---

## Level Summary

| Level | Service | Port | Format |
|-------|---------|------|--------|
| ★★★★ | api | 5000 | REST API / JSON |
| ★★★★★ | fuseki | 3030 | RDF / SPARQL |
| ★★★★★★ | (local) | - | Parquet / JSONL / Embeddings |
