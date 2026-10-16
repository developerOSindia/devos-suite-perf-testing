"""
Pure business logic for API payload size analysis, compression estimation, and performance profiling.
Zero Streamlit or UI dependencies.
"""

import gzip
from typing import Dict, Any


def analyze_payload_compression(payload: str) -> Dict[str, Any]:
    """Analyzes raw payload size and computes gzip compressed size and transfer metrics."""
    raw_bytes = (payload or "").encode("utf-8")
    raw_size = len(raw_bytes)

    if raw_size == 0:
        return {
            "raw_bytes": 0,
            "gzip_bytes": 0,
            "compression_ratio": "0.0%",
            "bytes_saved": 0,
            "latency_estimate_3g_ms": 0.0,
            "latency_estimate_5g_ms": 0.0,
        }

    gzip_bytes = len(gzip.compress(raw_bytes))
    savings = raw_size - gzip_bytes
    ratio = (savings / raw_size) * 100 if raw_size > 0 else 0.0

    # Theoretical transfer estimates (excluding TCP handshake / RTT)
    # 3G average: 1.5 Mbps (~187,500 bytes/sec)
    # 5G average: 50 Mbps (~6,250,000 bytes/sec)
    transfer_3g_ms = round((gzip_bytes / 187500) * 1000, 2)
    transfer_5g_ms = round((gzip_bytes / 6250000) * 1000, 2)

    return {
        "raw_bytes": raw_size,
        "gzip_bytes": gzip_bytes,
        "compression_ratio": f"{round(ratio, 1)}%",
        "bytes_saved": max(0, savings),
        "latency_estimate_3g_ms": transfer_3g_ms,
        "latency_estimate_5g_ms": transfer_5g_ms,
    }


def calculate_throughput_metrics(
    total_requests: int,
    duration_seconds: float,
    avg_payload_bytes: int = 1024,
) -> Dict[str, Any]:
    """Calculates Requests Per Second (RPS) and bandwidth consumption."""
    if duration_seconds <= 0:
        return {"rps": 0.0, "total_mb": 0.0, "bandwidth_mbps": 0.0}

    rps = round(total_requests / duration_seconds, 2)
    total_bytes = total_requests * avg_payload_bytes
    total_mb = round(total_bytes / (1024 * 1024), 3)
    bandwidth_mbps = round((total_bytes * 8) / (duration_seconds * 1_000_000), 2)

    return {
        "rps": rps,
        "total_requests": total_requests,
        "duration_seconds": duration_seconds,
        "total_mb": total_mb,
        "bandwidth_mbps": bandwidth_mbps,
    }
