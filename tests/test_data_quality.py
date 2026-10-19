import unittest
import json
from pathlib import Path

from scripts.build import serialize_payload
from scripts.data_quality import format_report, has_errors, inspect_csv


ROOT = Path(__file__).resolve().parents[1]


class DataQualityTest(unittest.TestCase):
    def test_sample_csv_passes_quality_checks(self):
        diagnostics = inspect_csv(ROOT / "data" / "sample_prices.csv")
        self.assertEqual(diagnostics["rows"], 36)
        self.assertEqual(diagnostics["missing_columns"], [])
        self.assertEqual(diagnostics["missing_values"], {})
        self.assertEqual(diagnostics["duplicate_keys"], [])
        self.assertEqual(diagnostics["invalid_months"], [])
        self.assertEqual(diagnostics["invalid_values"], [])
        self.assertEqual(diagnostics["non_positive_values"], [])
        self.assertFalse(diagnostics["empty_data"])
        self.assertFalse(has_errors(diagnostics))
        self.assertIn("Result: PASS", format_report(diagnostics))

    def test_reports_missing_values_duplicate_keys_and_invalid_months(self):
        diagnostics = inspect_csv(ROOT / "tests" / "fixtures" / "invalid_prices.csv")

        self.assertEqual(diagnostics["missing_values"], {"item_name": [3]})
        self.assertEqual(diagnostics["duplicate_keys"][0]["lines"], [2, 3])
        self.assertEqual(diagnostics["invalid_months"], [
            {"line": 2, "value": "2025-13"}, {"line": 3, "value": "2025-13"},
        ])
        report = format_report(diagnostics)
        self.assertIn("Missing values: 1", report)
        self.assertIn("Duplicate month/item_code keys: 1", report)
        self.assertIn("Invalid month values: 2", report)
        self.assertIn("Result: FAIL", report)
        self.assertTrue(has_errors(diagnostics))

    def test_reports_missing_required_columns(self):
        diagnostics = inspect_csv(ROOT / "tests" / "fixtures" / "missing_columns.csv")
        self.assertEqual(
            diagnostics["missing_columns"], ["item_name", "index_value", "source"]
        )

    def test_reports_non_numeric_non_finite_and_non_positive_values(self):
        diagnostics = inspect_csv(ROOT / "tests" / "fixtures" / "invalid_values.csv")
        self.assertEqual([row["line"] for row in diagnostics["invalid_values"]], [2, 3])
        self.assertEqual([row["line"] for row in diagnostics["non_positive_values"]], [4, 5])
        self.assertIn("Invalid index values: 2", format_report(diagnostics))
        self.assertIn("Non-positive index values: 2", format_report(diagnostics))
        self.assertTrue(has_errors(diagnostics))

    def test_empty_dataset_fails(self):
        diagnostics = inspect_csv(ROOT / "tests" / "fixtures" / "empty_prices.csv")
        self.assertTrue(diagnostics["empty_data"])
        self.assertTrue(has_errors(diagnostics))
        self.assertIn("Empty dataset: yes", format_report(diagnostics))

    def test_inline_payload_escapes_script_and_line_separator_characters(self):
        records = [{"name": "</script><script>alert(1)</script>\u2028"}]
        payload = serialize_payload(records)
        self.assertNotIn("<", payload)
        self.assertIn("\\u003c/script>", payload)
        self.assertIn("\\u2028", payload)
        self.assertEqual(json.loads(payload), records)


if __name__ == "__main__":
    unittest.main()
