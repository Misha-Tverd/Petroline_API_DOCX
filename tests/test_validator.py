import unittest

from validator import get_missing_required_fields


class ValidatorTest(unittest.TestCase):
    def test_returns_empty_list_when_required_fields_are_present(self):
        record = {
            "id": 123,
            "driver": "Driver",
            "vehicle": "Vehicle",
            "fuel": "Diesel",
            "amount": 10,
            "date": "2026-04-22T14:43:05",
            "azs": "AZS 1",
        }

        self.assertEqual(get_missing_required_fields(record), [])

    def test_returns_missing_fields_for_none_and_blank_values(self):
        record = {
            "id": "",
            "driver": "   ",
            "vehicle": None,
            "fuel": "Diesel",
            "amount": 0,
            "date": "2026-04-22T14:43:05",
            "azs": "AZS 1",
        }

        self.assertEqual(
            get_missing_required_fields(record),
            ["id", "driver", "vehicle"],
        )


if __name__ == "__main__":
    unittest.main()
