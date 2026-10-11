import unittest
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status, work_queue


class WorkflowTests(unittest.TestCase):
    def make_tickets(self):
        tickets = []
        create_ticket(tickets, "Small issue", "Other", "low", 1)
        create_ticket(tickets, "Big outage", "Network", "high", 12)
        create_ticket(tickets, "Many users", "Software", "low", 4)
        return tickets

    def test_unassigned_cannot_start(self):
        tickets = self.make_tickets()
        with self.assertRaises(ValueError):
            change_status(tickets, "T001", "in_progress")
        self.assertEqual(tickets[0]["status"], "open")

    def test_assigned_lifecycle(self):
        tickets = self.make_tickets()
        assign_ticket(tickets, "T001", " Ada ")
        change_status(tickets, "T001", "in_progress")
        change_status(tickets, "T001", "resolved")
        self.assertEqual(tickets[0]["status"], "resolved")
        with self.assertRaises(ValueError):
            change_status(tickets, "T001", "in_progress")
        change_status(tickets, "T001", "open")
        self.assertEqual(tickets[0]["status"], "open")

    def test_queue_priority_then_numeric_id(self):
        tickets = self.make_tickets()
        queue = work_queue(tickets)
        self.assertEqual([t["id"] for t in queue], ["T002", "T003", "T001"])

    def test_unknown_ticket_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.make_tickets(), "T999", "Ada")


if __name__ == "__main__":
    unittest.main()