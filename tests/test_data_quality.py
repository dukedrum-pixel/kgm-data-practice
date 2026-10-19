import unittest
from pathlib import Path

from scripts.data_quality import format_report, inspect_csv


ROOT = Path(__file__).resolve().parents[1]


class DataQualityTest(unittest.TestCase):
    def test_sample_csv_passes_quality_checks(self):
        diagnostics = inspect_csv(ROOT / "data" / "sample_prices.csv")
        self.assertEqual(diagnostics["rows"], 36)
        self.assertEqual(diagnostics["missing_columns"], [])
        self.assertEqual(diagnostics["missing_values"], {})
        self.assertEqual(diagnostics["duplicate_keys"], [])
        self.assertEqual(diagnostics["invalid_months"], [])
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

    def test_reports_missing_required_columns(self):
        diagnostics = inspect_csv(ROOT / "tests" / "fixtures" / "missing_columns.csv")
        self.assertEqual(
            diagnostics["missing_columns"], ["item_name", "index_value", "source"]
        )


if __name__ == "__main__":
    unittest.main()
