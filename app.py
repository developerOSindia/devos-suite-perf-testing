"""
DeveloperOS Performance & Benchmark Suite - Interactive Application
"""

import streamlit as st
from core.payload_analyzer import analyze_payload_compression
from ui.components import render_suite_header, render_suite_footer, render_main_promotional_banner

st.set_page_config(
    page_title="DeveloperOS - Performance Suite",
    page_icon="⚡",
    layout="wide",
)


def main():
    render_suite_header(
        title="API Payload Compression & Transfer Estimator",
        description="Estimate real Gzip compression efficiency, byte savings, and global mobile network transfer latency for API responses.",
    )

    sample_payload = '{\n  "status": "success",\n  "code": 200,\n  "data": [\n' + ",\n".join([f'    {{"id": {i}, "user": "dev_{i}", "active": true, "roles": ["developer", "admin"]}}' for i in range(25)]) + '\n  ]\n}'

    raw_payload = st.text_area("Input API Payload (JSON, HTML, or Text):", value=sample_payload, height=160)

    if raw_payload:
        stats = analyze_payload_compression(raw_payload)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Raw Size", f"{stats['raw_bytes']} B")
        col2.metric("Gzip Size", f"{stats['gzip_bytes']} B")
        col3.metric("Bandwidth Saved", stats["compression_ratio"])
        col4.metric("Bytes Saved", f"{stats['bytes_saved']} B")

        st.divider()
        st.subheader("Simulated Mobile Transfer Latency")
        col_3g, col_5g = st.columns(2)
        col_3g.info(f"📶 **3G Network Transfer:** ~{stats['latency_estimate_3g_ms']} ms")
        col_5g.success(f"⚡ **5G / Fiber Transfer:** ~{stats['latency_estimate_5g_ms']} ms")

    render_main_promotional_banner()
    render_suite_footer()


if __name__ == "__main__":
    main()
