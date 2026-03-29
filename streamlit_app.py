import requests
import streamlit as st
import pandas as pd

API_BASE = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 120

st.set_page_config(
    page_title="EvalBench",
    layout="wide",
)

st.title("EvalBench")
st.caption(
    "An LLM evaluation framework for measuring correctness, format compliance, and latency across benchmark tasks."
)


def call_evaluate_api():
    response = requests.post(
        f"{API_BASE}/evaluate",
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def render_summary(summary: dict):
    st.subheader("Benchmark Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Correctness Pass Rate", summary.get("correctness_pass_rate", 0.0))
    col2.metric("Format Pass Rate", summary.get("format_pass_rate", 0.0))
    col3.metric("Average Latency (s)", summary.get("average_latency_seconds", 0.0))

    st.write(f"Total Examples: {summary.get('total_examples', 0)}")

    st.subheader("Task Type Breakdown")
    breakdown = summary.get("task_type_breakdown", {})
    if breakdown:
        breakdown_rows = []
        for task_type, stats in breakdown.items():
            breakdown_rows.append({
                "task_type": task_type,
                "count": stats.get("count", 0),
                "correctness_pass_rate": stats.get("correctness_pass_rate", 0.0),
                "format_pass_rate": stats.get("format_pass_rate", 0.0),
            })
        st.dataframe(pd.DataFrame(breakdown_rows), use_container_width=True)
    else:
        st.info("No task breakdown available.")


def render_results(results: list):
    st.subheader("Per-Example Results")

    table_rows = []
    for item in results:
        table_rows.append({
            "id": item.get("id"),
            "task_type": item.get("task_type"),
            "latency_seconds": item.get("latency_seconds"),
            "correctness_passed": item.get("correctness", {}).get("passed"),
            "format_passed": item.get("format_check", {}).get("passed"),
            "predicted_output": item.get("predicted_output"),
        })

    st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

    st.subheader("Detailed Output")
    for item in results:
        with st.expander(f"Example {item.get('id')} | {item.get('task_type')}"):
            st.write("**Input**")
            st.write(item.get("input"))

            st.write("**Expected Output**")
            st.json(item.get("expected_output"))

            st.write("**Predicted Output**")
            st.code(item.get("predicted_output", ""), language="text")

            st.write("**Correctness**")
            st.json(item.get("correctness", {}))

            st.write("**Format Check**")
            st.json(item.get("format_check", {}))

            st.write(f"**Latency:** {item.get('latency_seconds')}s")


with st.sidebar:
    st.header("System")
    st.write("Make sure the FastAPI backend is running before evaluating.")
    st.code("python -m uvicorn app.main:app --reload", language="bash")


if st.button("Run Benchmark", use_container_width=True):
    try:
        with st.spinner("Running evaluation benchmark..."):
            result = call_evaluate_api()

        render_summary(result.get("summary", {}))
        render_results(result.get("results", []))

    except requests.exceptions.RequestException as exc:
        st.error(f"Could not connect to backend: {exc}")
    except Exception as exc:
        st.error(f"Unexpected error: {exc}")