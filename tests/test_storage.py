import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from storage import read_json_list, write_json_list


class StorageTest(unittest.TestCase):
    def test_read_json_list_returns_empty_list_for_missing_file(self):
        self.assertEqual(read_json_list("missing-file.json"), [])

    def test_read_json_list_returns_empty_list_for_non_list_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "data.json"
            path.write_text(json.dumps({"id": 1}), encoding="utf-8")

            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(read_json_list(path), [])

    def test_write_json_list_creates_parent_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "nested" / "data.json"
            data = [{"id": 1}]

            write_json_list(data, path)

            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), data)


if __name__ == "__main__":
    unittest.main()
