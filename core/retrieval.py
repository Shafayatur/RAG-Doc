import os
import time
from groq import Groq
from core.ingestion import get_collection
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

TOP_K = 8

def search_chunks(query: str) -> list[dict]:
    collection = get_collection()
    results = collection.query(
        query_texts=[query],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"]
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i].get("source", "unknown"),
            "chunk_index": results["metadatas"][0][i].get("chunk_index", 0),
            "distance": results["distances"][0][i]
        })
    return chunks

def generate_answer(question: str, chunks: list[dict]) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    context = "\n\n".join([
        f"[Source: {c['source']}, chunk {c['chunk_index']}]\n{c['text']}"
        for c in chunks
    ])

    prompt = f"""You are a precise document analyst. Your job is to answer questions 
based strictly on the provided document chunks below.

Rules:
- Read ALL chunks carefully before answering
- If counting things (projects, skills, years), go through each chunk systematically
- Always cite which document and chunk your answer comes from
- If the answer spans multiple chunks, combine the information
- If you truly cannot find the answer, say exactly what you looked for and couldn't find
- Never make up information

Document chunks:
{context}

Question: {question}

Answer (be specific and cite sources):"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.1
    )
    return response.choices[0].message.content

def ask(question: str) -> dict:
    start = time.time()
    chunks = search_chunks(question)
    answer = generate_answer(question, chunks)
    latency = round(time.time() - start, 2)
    sources = list(set(c["source"] for c in chunks))
    return {
        "answer": answer,
        "chunks": chunks,
        "sources": sources,
        "latency": latency
    }