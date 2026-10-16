"""
Unit tests for suite-perf-testing business logic.
"""

import sys
import unittest
from pathlib import Path

# Ensure suite root is in sys.path
SUITE_ROOT = Path(__file__).resolve().parent.parent
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from core.payload_analyzer import analyze_payload_compression


class TestPayloadAnalyzer(unittest.TestCase):
    def test_compression_savings(self):
        repetitive_json = '{"status": "ok", "items": [' + ', '.join(['{"id": %d}' % i for i in range(100)]) + ']}'
        res = analyze_payload_compression(repetitive_json)
        self.assertGreater(res["raw_bytes"], 0)
        self.assertLess(res["gzip_bytes"], res["raw_bytes"])
        self.assertGreater(res["bytes_saved"], 0)
        self.assertIn("%", res["compression_ratio"])

    def test_empty_payload(self):
        res = analyze_payload_compression("")
        self.assertEqual(res["raw_bytes"], 0)
        self.assertEqual(res["gzip_bytes"], 0)


if __name__ == "__main__":
    unittest.main()
