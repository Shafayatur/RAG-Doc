# DocMind — RAG Document Intelligence

Ask questions across multiple documents and get cited, grounded answers powered by LLaMA 3.3 70B.

## What it does
Upload PDF, DOCX, or TXT files → ask anything → get answers with source citations and chunk-level references. Every query is logged and visualized in an analytics dashboard.

## Architecture
Document → Parse → Chunk → Embed (HuggingFace) → ChromaDB
Query → Embed → Cosine Similarity Search → Top-8 Chunks → LLaMA 3.3 70B → Answer
Every query → SQLite log → Plotly dashboard

## Stack
| Layer | Technology |
|---|---|
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | ChromaDB |
| LLM | LLaMA 3.3 70B via Groq API |
| Observability | SQLite + Plotly |
| UI | Streamlit |

## Run locally
```bash
git clone https://github.com/Shafayatur/RAG-Doc
cd RAG-Doc
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key" > .env
python -m streamlit run app.py
```

