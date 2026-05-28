import sqlite3
import os
from datetime import datetime

DB_PATH = "logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            chunks_retrieved INTEGER,
            source_files TEXT,
            latency_seconds REAL
        )
    """)
    conn.commit()
    conn.close()

def log_query(question, answer, chunks_retrieved, source_files, latency_seconds):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO query_logs 
        (timestamp, question, answer, chunks_retrieved, source_files, latency_seconds)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        question,
        answer,
        chunks_retrieved,
        ", ".join(source_files) if source_files else "",
        latency_seconds
    ))
    conn.commit()
    conn.close()

def get_all_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM query_logs ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_log_count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM query_logs")
    count = cursor.fetchone()[0]
    conn.close()
    return count