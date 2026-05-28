import streamlit as st
import tempfile
import os
from core.ingestion import ingest_file, get_ingested_files, delete_file
from core.retrieval import ask
from core.database import log_query, init_db

init_db()

st.set_page_config(page_title="Chat — DocMind", page_icon="💬", layout="wide")

st.markdown("""
<style>
    .source-chip {
        background: #e8f4f8;
        border-radius: 8px;
        padding: 3px 10px;
        font-size: 0.8rem;
        color: #1a6b8a;
        margin-right: 5px;
        font-weight: 500;
    }
    .latency-tag {
        color: #999;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("💬 Chat")

with st.sidebar:
    st.header("📄 Documents")

    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["pdf", "docx", "txt", "md"],
        help="Supported: PDF, DOCX, TXT, MD"
    )

    if uploaded_file:
        with st.spinner(f"Ingesting {uploaded_file.name}..."):
            suffix = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            try:
                num_chunks = ingest_file(tmp_path, uploaded_file.name)
                st.success(f"✅ {uploaded_file.name}\n{num_chunks} chunks indexed")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                os.unlink(tmp_path)

    st.divider()
    files = get_ingested_files()

    if not files:
        st.caption("No documents yet.")
    else:
        st.caption(f"{len(files)} document(s) loaded")
        for f in files:
            col1, col2 = st.columns([4, 1])
            col1.caption(f"📎 {f}")
            if col2.button("🗑", key=f"del_{f}"):
                delete_file(f)
                st.rerun()

    st.divider()
    st.caption("**How it works**")
    st.caption("Your question is embedded and matched against document chunks via cosine similarity. Top matches are passed to LLaMA 3.3 70b as context.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.info("👆 Upload a document in the sidebar, then ask anything about it below.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            cols = st.columns([3, 1])
            with cols[0]:
                for s in msg["sources"]:
                    st.markdown(f'<span class="source-chip">📎 {s}</span>', unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f'<span class="latency-tag">⏱ {msg["latency"]}s</span>', unsafe_allow_html=True)
            with st.expander("View retrieved chunks"):
                for chunk in msg["chunks"]:
                    st.markdown(f"**{chunk['source']}** · chunk {chunk['chunk_index']} · distance `{chunk['distance']:.3f}`")
                    st.caption(chunk["text"][:400] + "...")
                    st.divider()

question = st.chat_input("Ask a question about your documents...")

if question:
    files = get_ingested_files()
    if not files:
        st.warning("Please upload at least one document first.")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching documents and generating answer..."):
                result = ask(question)

            st.markdown(result["answer"])

            cols = st.columns([3, 1])
            with cols[0]:
                for s in result["sources"]:
                    st.markdown(f'<span class="source-chip">📎 {s}</span>', unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f'<span class="latency-tag">⏱ {result["latency"]}s</span>', unsafe_allow_html=True)

            with st.expander("View retrieved chunks"):
                for chunk in result["chunks"]:
                    st.markdown(f"**{chunk['source']}** · chunk {chunk['chunk_index']} · distance `{chunk['distance']:.3f}`")
                    st.caption(chunk["text"][:400] + "...")
                    st.divider()

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"],
            "chunks": result["chunks"],
            "latency": result["latency"]
        })

        log_query(
            question=question,
            answer=result["answer"],
            chunks_retrieved=len(result["chunks"]),
            source_files=result["sources"],
            latency_seconds=result["latency"]
        )