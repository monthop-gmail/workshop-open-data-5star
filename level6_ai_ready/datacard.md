# Data Card: สถิติการใช้พลังงานไฟฟ้าตามภูมิภาค

## Overview

| Field | Value |
|-------|-------|
| **Dataset Name** | Thailand Regional Electricity Consumption Statistics |
| **Version** | 1.0.0 |
| **Last Updated** | 2567-01-15 |
| **License** | Open Government License - Thailand |
| **Source** | กรมพัฒนาพลังงานทดแทนและอนุรักษ์พลังงาน (พพ.) |
| **Language** | Thai (th), English (en) |

---

## Dataset Description

### Purpose
สถิติการใช้พลังงานไฟฟ้าแยกตามภูมิภาคของประเทศไทย สำหรับใช้ในการวิเคราะห์และพยากรณ์ความต้องการพลังงาน

### Intended Use Cases
- ✅ การวิเคราะห์แนวโน้มการใช้พลังงาน
- ✅ การพยากรณ์ความต้องการไฟฟ้า (Demand Forecasting)
- ✅ การเปรียบเทียบระหว่างภูมิภาค
- ✅ RAG (Retrieval-Augmented Generation) สำหรับ Q&A
- ✅ Fine-tuning LLM สำหรับโดเมนพลังงาน

### Out-of-Scope Uses
- ❌ การระบุตัวบุคคล (ไม่มีข้อมูลส่วนบุคคล)
- ❌ การตัดสินใจทางการเงินโดยตรง (ควรใช้ร่วมกับข้อมูลอื่น)

---

## Data Schema

### Features

| Column | Type | Description | Unit | Example |
|--------|------|-------------|------|---------|
| `region_code` | string | รหัสภูมิภาค (ISO-like) | - | TH-NE |
| `region_th` | string | ชื่อภูมิภาค (ไทย) | - | ภาคตะวันออกเฉียงเหนือ |
| `region_en` | string | ชื่อภูมิภาค (อังกฤษ) | - | Northeast |
| `year` | integer | ปี พ.ศ. | - | 2566 |
| `consumption_gwh` | float | ปริมาณการใช้ไฟฟ้า | GWh | 22180.0 |
| `customers` | integer | จำนวนผู้ใช้ไฟฟ้า | ราย | 7890000 |
| `growth_rate` | float | อัตราการเติบโต | % | 4.1 |
| `consumption_per_capita` | float | การใช้ไฟฟ้าต่อหัว | kWh/person | 2812.5 |
| `avg_monthly_bill` | float | ค่าไฟเฉลี่ยต่อเดือน | THB | 1250.0 |

### Data Types (for ML)
```python
{
    "region_code": "category",      # Categorical feature
    "region_th": "text",            # Text feature (Thai)
    "region_en": "text",            # Text feature (English)
    "year": "int64",                # Temporal feature
    "consumption_gwh": "float64",   # Target variable (regression)
    "customers": "int64",           # Numerical feature
    "growth_rate": "float64",       # Numerical feature
    "consumption_per_capita": "float64",
    "avg_monthly_bill": "float64"
}
```

---

## Data Quality

### Completeness
| Metric | Value |
|--------|-------|
| Total Records | 5 |
| Missing Values | 0% |
| Duplicate Records | 0 |

### Validation Rules
```python
# ค่าที่ต้องผ่าน validation
assert consumption_gwh > 0
assert customers > 0
assert 0 <= growth_rate <= 100
assert year >= 2500  # พ.ศ.
assert region_code in ["TH-C", "TH-N", "TH-NE", "TH-S", "TH-E"]
```

### Data Lineage
```
Raw Data (กฟภ., กฟน.)
    ↓
Aggregation (พพ.)
    ↓
Validation & Cleaning
    ↓
Published Dataset (data.go.th)
    ↓
AI-Ready Format (this dataset)
```

---

## Statistical Summary

| Metric | consumption_gwh | customers | growth_rate |
|--------|-----------------|-----------|-------------|
| count | 5 | 5 | 5 |
| mean | 26,090 | 5,400,000 | 3.58 |
| std | 11,847 | 2,567,890 | 1.08 |
| min | 15,620 | 2,987,000 | 2.5 |
| max | 45,230 | 8,542,000 | 5.3 |

---

## Known Limitations & Biases

### Limitations
1. **Temporal Coverage**: ข้อมูลปี 2566 เท่านั้น ไม่มี time series
2. **Granularity**: ระดับภูมิภาค ไม่มีระดับจังหวัด
3. **Sample Size**: 5 records (5 ภูมิภาค) - เหมาะกับ demo ไม่ใช่ production ML

### Potential Biases
- ภาคตะวันออกมี consumption/capita สูง เพราะมีโรงงานอุตสาหกรรมมาก
- ไม่รวมการไฟฟ้านครหลวง (กทม.) แยกต่างหาก

### Recommended Mitigations
- ใช้ร่วมกับข้อมูล GDP รายภูมิภาค
- ปรับ normalize ด้วยจำนวนประชากร
- เพิ่มข้อมูลหลายปีสำหรับ time series analysis

---

## File Formats Available

| Format | File | Size | Use Case |
|--------|------|------|----------|
| Parquet | `energy_stats.parquet` | ~2 KB | Big data, Spark, Pandas |
| JSONL | `energy_stats.jsonl` | ~3 KB | LLM fine-tuning, streaming |
| CSV | `energy_stats_clean.csv` | ~1 KB | General purpose |
| Embeddings | `embeddings.json` | ~5 KB | Vector search, RAG |

---

## Usage Examples

### Pandas
```python
import pandas as pd
df = pd.read_parquet("data/energy_stats.parquet")
```

### Scikit-learn
```python
from sklearn.preprocessing import StandardScaler
X = df[["customers", "growth_rate"]].values
scaler = StandardScaler().fit(X)
```

### LangChain RAG
```python
from langchain.vectorstores import FAISS
vectorstore = FAISS.load_local("data/vectorstore")
retriever = vectorstore.as_retriever()
```

---

## Ethical Considerations

### Privacy
- ✅ ไม่มีข้อมูลส่วนบุคคล (PII)
- ✅ ข้อมูลระดับ aggregate เท่านั้น

### Fairness
- ⚠️ ข้อมูลไม่ครอบคลุมพื้นที่พิเศษ (เขตเศรษฐกิจพิเศษ)
- ⚠️ ควรใช้ร่วมกับข้อมูลเศรษฐกิจสังคม

### Environmental Impact
- Dataset ขนาดเล็ก ใช้ทรัพยากรน้อยในการประมวลผล

---

## Citation

```bibtex
@dataset{dede_energy_2566,
  title = {Thailand Regional Electricity Consumption Statistics 2566},
  author = {Department of Alternative Energy Development and Efficiency},
  year = {2024},
  publisher = {data.go.th},
  version = {1.0.0},
  url = {https://github.com/monthop-gmail/workshop-open-data-5star}
}
```

---

## Contact

- **Data Owner**: กรมพัฒนาพลังงานทดแทนและอนุรักษ์พลังงาน (พพ.)
- **Technical Contact**: workshop@example.go.th
- **Last Review Date**: 2567-01-15
