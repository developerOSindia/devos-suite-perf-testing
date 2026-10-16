"""
Unit tests for suite-perf-testing payload compression and throughput.
"""

import sys
import unittest
from pathlib import Path

SUITE_ROOT = Path(__file__).resolve().parent.parent
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from core.payload_analyzer import analyze_payload_compression, calculate_throughput_metrics


class TestPayloadAnalyzer(unittest.TestCase):
    def test_compressible_payload(self):
        payload = '{"status": 200, "message": "success"} ' * 100
        res = analyze_payload_compression(payload)
        self.assertGreater(res["raw_bytes"], res["gzip_bytes"])
        self.assertGreater(res["bytes_saved"], 0)
        self.assertIn("%", res["compression_ratio"])
        self.assertGreater(res["latency_estimate_3g_ms"], 0)

    def test_empty_payload(self):
        res = analyze_payload_compression("")
        self.assertEqual(res["raw_bytes"], 0)
        self.assertEqual(res["gzip_bytes"], 0)
        self.assertEqual(res["bytes_saved"], 0)
        self.assertEqual(res["latency_estimate_3g_ms"], 0.0)

    def test_none_payload(self):
        res = analyze_payload_compression(None)
        self.assertEqual(res["raw_bytes"], 0)

    def test_throughput_standard(self):
        res = calculate_throughput_metrics(
            total_requests=10000,
            duration_seconds=10.0,
            avg_payload_bytes=2048,
        )
        self.assertEqual(res["rps"], 1000.0)
        self.assertGreater(res["total_mb"], 19.0)
        self.assertGreater(res["bandwidth_mbps"], 16.0)

    def test_throughput_zero_duration(self):
        res = calculate_throughput_metrics(total_requests=100, duration_seconds=0.0)
        self.assertEqual(res["rps"], 0.0)
        self.assertEqual(res["bandwidth_mbps"], 0.0)


if __name__ == "__main__":
    unittest.main()
