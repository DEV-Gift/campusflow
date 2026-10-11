import json
import tempfile
import unittest
from pathlib import Path
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket


class StorageTests(unittest.TestCase):
    def test_missing_file_starts_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(load_tickets(Path(directory) / "missing.json"), [])

    def test_save_and_reload(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            tickets = []
            create_ticket(tickets, "Wi-Fi down", "Network", "high", 12)
            save_tickets(path, tickets)
            self.assertEqual(load_tickets(path), tickets)
            create_ticket(tickets, "New laptop", "Hardware", "low", 1)
            self.assertEqual(tickets[-1]["id"], "T002")

    def test_malformed_json_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text("{bad json", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_duplicate_ids_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text(json.dumps([{"id": "T001"}, {"id": "T001"}]), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_tickets(path)


if __name__ == "__main__":
    unittest.main()