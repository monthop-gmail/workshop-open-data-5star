"""
Prepare AI-Ready Data
Level 6: แปลงข้อมูลให้พร้อมใช้กับ AI/ML

รัน: pip install pandas pyarrow sentence-transformers
     python prepare_data.py
"""

import json
from pathlib import Path

# Check dependencies
def check_dependencies():
    missing = []
    try:
        import pandas
    except ImportError:
        missing.append("pandas")
    try:
        import pyarrow
    except ImportError:
        missing.append("pyarrow")

    if missing:
        print(f"Missing dependencies: {missing}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    return True


def load_jsonl(filepath: str) -> list:
    """Load JSONL file"""
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line.strip()))
    return records


def create_parquet(records: list, output_path: str):
    """สร้างไฟล์ Parquet"""
    import pandas as pd

    df = pd.DataFrame(records)

    # Set proper dtypes
    df["region_code"] = df["region_code"].astype("category")
    df["year"] = df["year"].astype("int64")
    df["consumption_gwh"] = df["consumption_gwh"].astype("float64")
    df["customers"] = df["customers"].astype("int64")
    df["growth_rate"] = df["growth_rate"].astype("float64")

    # Save as Parquet
    df.to_parquet(output_path, engine="pyarrow", index=False)
    print(f"✅ Created Parquet: {output_path}")
    print(f"   Shape: {df.shape}")
    print(f"   Size: {Path(output_path).stat().st_size:,} bytes")


def create_embeddings(records: list, output_path: str):
    """สร้าง text embeddings (ถ้ามี sentence-transformers)"""
    try:
        from sentence_transformers import SentenceTransformer
        print("\nGenerating embeddings with SentenceTransformer...")

        model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

        texts = [r.get("text_description", r["region_th"]) for r in records]
        embeddings = model.encode(texts)

        # Save embeddings with metadata
        embedding_data = []
        for i, record in enumerate(records):
            embedding_data.append({
                "region_code": record["region_code"],
                "region_th": record["region_th"],
                "text": texts[i],
                "embedding": embeddings[i].tolist()
            })

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(embedding_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Created Embeddings: {output_path}")
        print(f"   Embedding dim: {len(embeddings[0])}")

    except ImportError:
        print("\n⚠️  sentence-transformers not installed")
        print("   Install with: pip install sentence-transformers")
        print("   Creating placeholder embeddings instead...")

        # Create placeholder embeddings
        embedding_data = []
        for record in records:
            embedding_data.append({
                "region_code": record["region_code"],
                "region_th": record["region_th"],
                "text": record.get("text_description", record["region_th"]),
                "embedding": [0.0] * 384,  # Placeholder
                "note": "Placeholder - install sentence-transformers for real embeddings"
            })

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(embedding_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Created Placeholder Embeddings: {output_path}")


def create_huggingface_dataset(records: list, output_dir: str):
    """สร้าง HuggingFace Dataset format"""
    try:
        from datasets import Dataset

        dataset = Dataset.from_list(records)
        dataset.save_to_disk(output_dir)
        print(f"✅ Created HuggingFace Dataset: {output_dir}")

    except ImportError:
        print("\n⚠️  datasets library not installed")
        print("   Install with: pip install datasets")


def print_summary(records: list):
    """แสดงสรุปข้อมูล"""
    import pandas as pd

    df = pd.DataFrame(records)

    print("\n" + "=" * 60)
    print("DATA SUMMARY")
    print("=" * 60)

    print(f"\nRecords: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    print("\nNumerical Statistics:")
    print(df[["consumption_gwh", "customers", "growth_rate"]].describe())

    print("\nRegions:")
    for _, row in df.iterrows():
        print(f"  {row['region_code']}: {row['region_th']} - {row['consumption_gwh']:,.0f} GWh")


def main():
    print("=" * 60)
    print("PREPARING AI-READY DATA (Level 6)")
    print("=" * 60)

    if not check_dependencies():
        return 1

    data_dir = Path(__file__).parent / "data"
    jsonl_path = data_dir / "energy_stats.jsonl"

    # Load data
    print(f"\nLoading data from {jsonl_path}...")
    records = load_jsonl(jsonl_path)
    print(f"Loaded {len(records)} records")

    # Create Parquet
    print("\n--- Creating Parquet ---")
    create_parquet(records, str(data_dir / "energy_stats.parquet"))

    # Create Embeddings
    print("\n--- Creating Embeddings ---")
    create_embeddings(records, str(data_dir / "embeddings.json"))

    # Create HuggingFace Dataset (optional)
    print("\n--- Creating HuggingFace Dataset ---")
    create_huggingface_dataset(records, str(data_dir / "hf_dataset"))

    # Print summary
    print_summary(records)

    print("\n" + "=" * 60)
    print("✅ AI-Ready data preparation complete!")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
