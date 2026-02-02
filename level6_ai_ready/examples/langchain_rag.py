"""
Example: RAG (Retrieval-Augmented Generation) with LangChain
Level 6: AI-Ready Government Data

รัน: pip install langchain langchain-community faiss-cpu sentence-transformers
     python langchain_rag.py

หมายเหตุ: ตัวอย่างนี้ใช้ local embeddings ไม่ต้องใช้ OpenAI API
"""

import json
from pathlib import Path


def load_documents():
    """โหลดข้อมูลเป็น documents"""
    data_dir = Path(__file__).parent.parent / "data"
    jsonl_path = data_dir / "energy_stats.jsonl"

    documents = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            # สร้าง document text
            doc_text = f"""
ข้อมูลสถิติพลังงานไฟฟ้า {record['region_th']} ({record['region_en']}) ปี {record['year']}

- รหัสภูมิภาค: {record['region_code']}
- ปริมาณการใช้ไฟฟ้า: {record['consumption_gwh']:,} GWh
- จำนวนผู้ใช้ไฟฟ้า: {record['customers']:,} ราย
- อัตราการเติบโต: {record['growth_rate']}%
- การใช้ไฟฟ้าต่อหัว: {record.get('consumption_per_capita', 'N/A')} kWh/คน
- ค่าไฟเฉลี่ยต่อเดือน: {record.get('avg_monthly_bill', 'N/A')} บาท

{record.get('text_description', '')}
""".strip()

            documents.append({
                "text": doc_text,
                "metadata": {
                    "region_code": record["region_code"],
                    "region_th": record["region_th"],
                    "year": record["year"]
                }
            })

    return documents


def create_vectorstore(documents):
    """สร้าง vector store จาก documents"""
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS
        from langchain.schema import Document

        print("Creating vector store...")

        # Create Document objects
        docs = [
            Document(page_content=d["text"], metadata=d["metadata"])
            for d in documents
        ]

        # Use local embeddings (no API needed)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        # Create FAISS vector store
        vectorstore = FAISS.from_documents(docs, embeddings)

        print(f"✅ Created vector store with {len(docs)} documents")

        return vectorstore

    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install with: pip install langchain langchain-community faiss-cpu sentence-transformers")
        return None


def simple_rag_demo(vectorstore):
    """Demo RAG แบบง่าย (ไม่ใช้ LLM)"""
    print("\n" + "=" * 60)
    print("SIMPLE RAG DEMO (Retrieval Only)")
    print("=" * 60)

    questions = [
        "ภูมิภาคไหนใช้ไฟฟ้ามากที่สุด",
        "ภาคอีสานมีการเติบโตเท่าไหร่",
        "ภาคตะวันออกมีผู้ใช้ไฟฟ้ากี่ราย",
    ]

    for question in questions:
        print(f"\n❓ Question: {question}")

        # Retrieve relevant documents
        docs = vectorstore.similarity_search(question, k=2)

        print("📄 Retrieved Documents:")
        for i, doc in enumerate(docs, 1):
            print(f"\n  [{i}] {doc.metadata['region_th']}")
            # Show first 200 chars
            preview = doc.page_content[:200] + "..."
            print(f"      {preview}")


def full_rag_demo(vectorstore):
    """Demo RAG แบบเต็ม (ใช้ LLM)"""
    print("\n" + "=" * 60)
    print("FULL RAG DEMO (with LLM)")
    print("=" * 60)

    try:
        from langchain.chains import RetrievalQA
        from langchain_community.llms import Ollama

        print("\nTrying to connect to Ollama...")

        # Use local LLM (Ollama)
        llm = Ollama(model="llama2", base_url="http://localhost:11434")

        # Create RAG chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
            return_source_documents=True
        )

        questions = [
            "ภูมิภาคไหนมีอัตราการเติบโตสูงสุด และเพราะอะไร",
            "เปรียบเทียบการใช้ไฟฟ้าระหว่างภาคกลางกับภาคอีสาน",
        ]

        for question in questions:
            print(f"\n❓ Question: {question}")

            result = qa_chain({"query": question})

            print(f"💡 Answer: {result['result']}")
            print(f"📚 Sources: {[d.metadata['region_th'] for d in result['source_documents']]}")

    except Exception as e:
        print(f"\n⚠️  Full RAG demo requires Ollama running locally")
        print(f"   Error: {e}")
        print("\nTo run full RAG demo:")
        print("  1. Install Ollama: https://ollama.ai")
        print("  2. Run: ollama pull llama2")
        print("  3. Run this script again")


def create_qa_dataset(documents):
    """สร้าง Q&A dataset สำหรับ fine-tuning"""
    print("\n" + "=" * 60)
    print("CREATING Q&A DATASET FOR FINE-TUNING")
    print("=" * 60)

    qa_pairs = []

    # Generate Q&A pairs from data
    for doc in documents:
        region = doc["metadata"]["region_th"]
        text = doc["text"]

        # Extract info
        lines = text.split("\n")
        consumption = None
        growth = None
        customers = None

        for line in lines:
            if "ปริมาณการใช้ไฟฟ้า" in line:
                consumption = line.split(":")[1].strip()
            elif "อัตราการเติบโต" in line:
                growth = line.split(":")[1].strip()
            elif "จำนวนผู้ใช้ไฟฟ้า" in line:
                customers = line.split(":")[1].strip()

        # Create Q&A pairs
        if consumption:
            qa_pairs.append({
                "instruction": f"{region}มีการใช้ไฟฟ้าเท่าไหร่ในปี 2566",
                "input": "",
                "output": f"{region}มีการใช้ไฟฟ้า {consumption} ในปี 2566"
            })

        if growth:
            qa_pairs.append({
                "instruction": f"อัตราการเติบโตของการใช้ไฟฟ้าใน{region}เป็นเท่าไหร่",
                "input": "",
                "output": f"{region}มีอัตราการเติบโตของการใช้ไฟฟ้า {growth}"
            })

    # Save as JSONL for fine-tuning
    output_path = Path(__file__).parent.parent / "data" / "qa_finetune.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for qa in qa_pairs:
            f.write(json.dumps(qa, ensure_ascii=False) + "\n")

    print(f"✅ Created {len(qa_pairs)} Q&A pairs")
    print(f"   Saved to: {output_path}")

    print("\nSample Q&A pairs:")
    for qa in qa_pairs[:3]:
        print(f"\n  Q: {qa['instruction']}")
        print(f"  A: {qa['output']}")


def main():
    print("=" * 60)
    print("LANGCHAIN RAG EXAMPLE - Level 6 AI-Ready Data")
    print("=" * 60)

    # Load documents
    documents = load_documents()
    print(f"\nLoaded {len(documents)} documents")

    # Create vector store
    vectorstore = create_vectorstore(documents)

    if vectorstore:
        # Simple RAG demo (retrieval only)
        simple_rag_demo(vectorstore)

        # Full RAG demo (with LLM)
        full_rag_demo(vectorstore)

    # Create Q&A dataset for fine-tuning
    create_qa_dataset(documents)

    print("\n" + "=" * 60)
    print("✅ RAG demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
