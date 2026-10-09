"""Ticket assignment, lifecycle, and work queue."""
from copy import deepcopy
from .tickets import PRIORITY_RANK


def _find_mutable(tickets, ticket_id):
    wanted = str(ticket_id).strip().upper()
    for ticket in tickets:
        if ticket.get("id", "").upper() == wanted:
            return ticket
    raise ValueError(f"unknown ticket ID: {ticket_id}")


def assign_ticket(tickets, ticket_id, staff_name):
    ticket = _find_mutable(tickets, ticket_id)
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("staff member name must not be blank.")
    ticket["assigned_to"] = staff_name.strip()
    return deepcopy(ticket)


def change_status(tickets, ticket_id, new_status):
    ticket = _find_mutable(tickets, ticket_id)
    status = str(new_status).strip().lower()
    if status not in {"open", "in_progress", "resolved"}:
        raise ValueError("status must be open, in_progress, or resolved.")
    current = ticket["status"]

    if current == "resolved":
        if status != "open":
            raise ValueError("resolved tickets must be explicitly reopened to open first.")
        ticket["status"] = "open"
        return deepcopy(ticket)

    if current == "open" and status == "in_progress":
        if not ticket.get("assigned_to"):
            raise ValueError("assign the ticket before moving it to in_progress.")
        ticket["status"] = "in_progress"
        return deepcopy(ticket)
    if current == "in_progress" and status == "resolved":
        ticket["status"] = "resolved"
        return deepcopy(ticket)
    if current == "open" and status == "open":
        return deepcopy(ticket)
    if current == "in_progress" and status == "in_progress":
        return deepcopy(ticket)
    raise ValueError(f"invalid status transition: {current} -> {status}")


def work_queue(tickets):
    unresolved = [t for t in tickets if t.get("status") != "resolved"]
    def numeric_id(ticket):
        value = str(ticket.get("id", "T0"))
        suffix = value[1:] if value.startswith("T") else ""
        return int(suffix) if suffix.isdigit() else float("inf")
    return deepcopy(sorted(unresolved, key=lambda t: (PRIORITY_RANK.get(t.get("priority"), 99), numeric_id(t))))