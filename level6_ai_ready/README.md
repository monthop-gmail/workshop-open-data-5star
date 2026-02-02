# ★★★★★★ Level 6: AI-Ready Government Data

## Overview

Level 6 เป็นการยกระดับ Open Data ให้พร้อมใช้งานกับ AI/ML โดยเพิ่ม:
- **Data Quality** - ข้อมูลสะอาด validated
- **ML-Optimized Formats** - Parquet, JSONL, Embeddings
- **AI Metadata** - Data Cards, Schema
- **Usage Examples** - พร้อมใช้งานทันที

```
Level 5: Linked Data      →      Level 6: AI-Ready
(เชื่อมโยงข้อมูล)                 (พร้อมใช้กับ AI/ML)
```

---

## File Structure

```
level6_ai_ready/
├── README.md                    # This file
├── datacard.md                  # AI Documentation (Data Card)
├── schema.json                  # JSON Schema + ML metadata
├── validation.py                # Data quality checks
├── prepare_data.py              # Generate Parquet/Embeddings
│
├── data/
│   ├── energy_stats.jsonl       # JSONL format (LLM fine-tuning)
│   ├── energy_stats_clean.csv   # Clean CSV
│   ├── energy_stats.parquet     # Parquet (generated)
│   ├── embeddings.json          # Vector embeddings (generated)
│   └── qa_finetune.jsonl        # Q&A pairs for fine-tuning
│
└── examples/
    ├── pandas_analysis.py       # Data analysis
    ├── sklearn_example.py       # ML training
    └── langchain_rag.py         # RAG example
```

---

## Quick Start

### 1. Validate Data
```bash
python validation.py
```

### 2. Prepare AI-Ready Formats
```bash
pip install pandas pyarrow sentence-transformers
python prepare_data.py
```

### 3. Run Examples
```bash
# Data Analysis
pip install pandas matplotlib
python examples/pandas_analysis.py

# Machine Learning
pip install pandas scikit-learn
python examples/sklearn_example.py

# RAG (Retrieval-Augmented Generation)
pip install langchain langchain-community faiss-cpu sentence-transformers
python examples/langchain_rag.py
```

---

## Data Formats

### JSONL (LLM Fine-tuning)
```json
{"region_code": "TH-NE", "region_th": "ภาคตะวันออกเฉียงเหนือ", "consumption_gwh": 22180, "text_description": "..."}
```

**Use cases:**
- Fine-tuning LLMs (GPT, LLaMA, etc.)
- Streaming data processing
- Line-by-line processing

### Parquet (Big Data)
```python
import pandas as pd
df = pd.read_parquet("data/energy_stats.parquet")
```

**Use cases:**
- Large-scale data analysis
- Spark/Dask processing
- Columnar queries

### Embeddings (Vector Search)
```json
{
  "region_code": "TH-NE",
  "text": "ภาคตะวันออกเฉียงเหนือ...",
  "embedding": [0.123, -0.456, ...]
}
```

**Use cases:**
- Semantic search
- RAG (Retrieval-Augmented Generation)
- Similarity matching

---

## AI Use Cases

### 1. Demand Forecasting
```python
# ใช้ historical data พยากรณ์ความต้องการไฟฟ้า
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(X_train, y_train)
```

### 2. RAG Q&A System
```python
# ตอบคำถามเกี่ยวกับข้อมูลพลังงาน
from langchain.chains import RetrievalQA
qa = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())
answer = qa.run("ภูมิภาคไหนใช้ไฟฟ้ามากที่สุด")
```

### 3. LLM Fine-tuning
```python
# Fine-tune LLM ให้เข้าใจโดเมนพลังงาน
from datasets import load_dataset
dataset = load_dataset("json", data_files="data/qa_finetune.jsonl")
```

### 4. Anomaly Detection
```python
# ตรวจจับความผิดปกติในการใช้ไฟฟ้า
from sklearn.ensemble import IsolationForest
detector = IsolationForest()
anomalies = detector.fit_predict(X)
```

---

## Data Quality

### Validation Rules
- ✅ No missing values
- ✅ Valid region codes
- ✅ Positive consumption values
- ✅ Growth rate within bounds
- ✅ No duplicate records

### Run Validation
```bash
python validation.py
```

Expected output:
```
DATA VALIDATION REPORT
Records checked: 5
✅ No errors found!
RESULT: ✅ PASSED - Data is AI-ready!
```

---

## Comparison: Level 5 vs Level 6

| Aspect | Level 5 (Linked Data) | Level 6 (AI-Ready) |
|--------|----------------------|-------------------|
| **Goal** | Link data across sources | Train/Run AI models |
| **Format** | RDF, Turtle, SPARQL | Parquet, JSONL, Vectors |
| **Query** | SPARQL | SQL, Vector Search |
| **Metadata** | Ontology, URIs | Data Cards, Schema |
| **Users** | Data Engineers | ML Engineers, Data Scientists |
| **Standards** | W3C Semantic Web | ML/AI best practices |

---

## Best Practices for AI-Ready Data

### 1. Data Quality
- Clean and validate data before publishing
- Document known issues and limitations
- Version your datasets

### 2. Documentation
- Include Data Cards with:
  - Intended use cases
  - Known biases
  - Ethical considerations

### 3. Formats
- Provide multiple formats for different use cases
- Include pre-computed embeddings for text data
- Use efficient columnar formats for large data

### 4. Examples
- Include working code examples
- Show common use cases
- Document dependencies

---

## References

- [Google Data Cards](https://research.google/pubs/pub48120/)
- [HuggingFace Dataset Cards](https://huggingface.co/docs/datasets/dataset_card)
- [ML Metadata Best Practices](https://www.tensorflow.org/tfx/guide/mlmd)
