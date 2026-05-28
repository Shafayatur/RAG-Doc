import streamlit as st
from core.database import init_db, get_log_count
from core.ingestion import get_ingested_files

init_db()

st.set_page_config(
    page_title="DocMind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .block-container { padding-top: 3rem; padding-bottom: 2rem; }
    .main-title {
        font-size: 2.8rem;
        font-weight: 900;
        letter-spacing: -1px;
        font-family: monospace;
        color: #2200ff;
        line-height: 1;
        overflow: hidden;
        white-space: nowrap;
    }
    .sub {
        font-size: 1rem;
        color: #666;
        font-family: monospace;
        margin-top: 6px;
        margin-bottom: 2rem;
    }
    .stat-box {
        background: #1A1A1A;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }
    .stat-number {
        font-size: 2.2rem;
        font-weight: 800;
        color: #2200ff;
        font-family: monospace;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #555;
        font-family: monospace;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .feature-box {
        background: #111;
        border: 1px solid #222;
        border-left: 3px solid #2200ff;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
    }
    .feature-box h4 {
        color: #2200ff;
        font-family: monospace;
        margin: 0 0 4px 0;
        font-size: 0.95rem;
    }
    .feature-box p {
        color: #666;
        font-size: 0.85rem;
        margin: 0;
        font-family: monospace;
    }
    .tech-pill {
        display: inline-block;
        background: #1a1a1a;
        border: 1px solid #333;
        color: #2200ff;
        border-radius: 4px;
        padding: 3px 10px;
        font-size: 0.75rem;
        font-family: monospace;
        margin: 3px;
    }
    .section-label {
        font-family: monospace;
        font-size: 0.7rem;
        color: #444;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">DOCMIND</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">// RAG-powered document intelligence — ask anything, get cited answers</div>', unsafe_allow_html=True)

files = get_ingested_files()
total_queries = get_log_count()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="stat-box"><div class="stat-number">{len(files)}</div><div class="stat-label">Documents loaded</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stat-box"><div class="stat-number">{total_queries}</div><div class="stat-label">Queries run</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-box"><div class="stat-number">70B</div><div class="stat-label">Model params</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-box"><div class="stat-number">∞</div><div class="stat-label">Context docs</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_a, col_b = st.columns([1, 1])

with col_a:
    st.markdown('<div class="section-label">// Pipeline</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-box">
        <h4>01 — INGEST</h4>
        <p>Parse PDF/DOCX/TXT → chunk (1000 chars) → embed via HuggingFace → store in ChromaDB</p>
    </div>
    <div class="feature-box">
        <h4>02 — RETRIEVE</h4>
        <p>Embed query → cosine similarity search → fetch top-8 chunks from vector store</p>
    </div>
    <div class="feature-box">
        <h4>03 — GENERATE</h4>
        <p>Pass chunks as context → LLaMA 3.3 70b via Groq → grounded answer with citations</p>
    </div>
    <div class="feature-box">
        <h4>04 — OBSERVE</h4>
        <p>Log query + latency + sources → SQLite → Plotly analytics dashboard</p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="section-label">// Stack</div>', unsafe_allow_html=True)
    techs = [
        "Python 3.11", "Streamlit", "ChromaDB",
        "sentence-transformers", "LLaMA 3.3 70b",
        "Groq API", "SQLite", "Plotly", "HuggingFace",
        "all-MiniLM-L6-v2", "python-dotenv", "pypdf"
    ]
    pills = "".join([f'<span class="tech-pill">{t}</span>' for t in techs])
    st.markdown(pills, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">// Get started</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-box">
        <h4>→ CHAT</h4>
        <p>Upload a document and start asking questions</p>
    </div>
    <div class="feature-box">
        <h4>→ ANALYTICS</h4>
        <p>View query patterns and document usage stats</p>
    </div>
    """, unsafe_allow_html=True)