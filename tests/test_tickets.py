import unittest
from campusflow.tickets import calculate_priority, create_ticket, get_ticket


class TicketTests(unittest.TestCase):
    def test_priority_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_priority_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_priority_medium_from_users(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_priority_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_zero_users_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("low", 0)

    def test_decimal_users_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("low", 2.5)

    def test_blank_title_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket([], "  ", "Network", "high", 1)

    def test_category_case_normalized_and_id_generated(self):
        tickets = []
        first = create_ticket(tickets, "Wi-Fi down", "nEtWoRk", "HIGH", 12)
        second = create_ticket(tickets, "Laptop broken", "Hardware", "low", 1)
        self.assertEqual(first["category"], "Network")
        self.assertEqual(first["id"], "T001")
        self.assertEqual(second["id"], "T002")
        self.assertEqual(get_ticket(tickets, "t001")["title"], "Wi-Fi down")


if __name__ == "__main__":
    unittest.main()