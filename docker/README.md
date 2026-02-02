# Docker Setup: 5-Star Open Data Workshop

## Services

| Service | Port | Description |
|---------|------|-------------|
| **web** | 8080 | Web UI + Slides |
| **api** | 5000 | REST API (Level 4) |
| **fuseki** | 3030 | SPARQL Endpoint (Level 5) |

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

| URL | Description |
|-----|-------------|
| http://localhost:8080 | Web UI (Demo) |
| http://localhost:8080/slides/ | Presentation Slides |
| http://localhost:5000 | API Documentation |
| http://localhost:5000/api/v1/energy/regions | API: ข้อมูลทุกภูมิภาค |
| http://localhost:3030 | Fuseki Admin UI |
| http://localhost:3030/#/dataset/energy/query | SPARQL Query UI |

---

## Level 4: REST API

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

## Level 5: SPARQL

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
           │   Level 4    │   │    Level 5     │
           │  REST API    │   │    SPARQL      │
           └──────────────┘   └───────┬────────┘
                                      │
                              ┌───────▼────────┐
                              │  RDF Data      │
                              │  (Turtle)      │
                              └────────────────┘
```

---

## Credentials

| Service | Username | Password |
|---------|----------|----------|
| Fuseki Admin | admin | admin123 |
