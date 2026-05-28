import streamlit as st
import pandas as pd
import plotly.express as px
from core.database import get_all_logs, get_log_count, init_db

init_db()

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")
st.title("📊 Query Analytics Dashboard")

logs = get_all_logs()

if not logs:
    st.info("No queries yet. Go to the Chat page and ask some questions first!")
    st.stop()

df = pd.DataFrame(logs, columns=[
    "id", "timestamp", "question", "answer",
    "chunks_retrieved", "source_files", "latency_seconds"
])
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date

# ── Top metrics ─────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Queries", get_log_count())
col2.metric("Avg Latency", f"{df['latency_seconds'].mean():.2f}s")
col3.metric("Avg Chunks/Query", f"{df['chunks_retrieved'].mean():.1f}")
col4.metric("Unique Days", df['date'].nunique())

st.divider()

# ── Charts ───────────────────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Queries over time")
    queries_by_date = df.groupby("date").size().reset_index(name="count")
    fig1 = px.line(
        queries_by_date, x="date", y="count",
        markers=True, labels={"date": "Date", "count": "Queries"}
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("Latency over time")
    fig2 = px.scatter(
        df, x="timestamp", y="latency_seconds",
        labels={"timestamp": "Time", "latency_seconds": "Latency (s)"},
        trendline="lowess"
    )
    st.plotly_chart(fig2, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Most queried documents")
    all_sources = []
    for sources in df["source_files"].dropna():
        all_sources.extend([s.strip() for s in sources.split(",")])
    source_df = pd.Series(all_sources).value_counts().reset_index()
    source_df.columns = ["document", "count"]
    fig3 = px.bar(
        source_df, x="count", y="document",
        orientation="h", labels={"count": "Times queried", "document": ""}
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    st.subheader("Chunks retrieved distribution")
    fig4 = px.histogram(
        df, x="chunks_retrieved",
        labels={"chunks_retrieved": "Chunks retrieved", "count": "Frequency"}
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── Query log table ──────────────────────────────────────────────────────────
st.subheader("Full query log")
st.dataframe(
    df[["timestamp", "question", "chunks_retrieved", "source_files", "latency_seconds"]],
    use_container_width=True,
    hide_index=True
)