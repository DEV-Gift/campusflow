"""Ticket creation, validation, lookup, and priority rules."""
from copy import deepcopy

CATEGORIES = {"network": "Network", "hardware": "Hardware", "software": "Software", "other": "Other"}
URGENCIES = {"low", "medium", "high"}
PRIORITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def calculate_priority(urgency, affected_users):
    """Apply the guide's priority rules in their required order."""
    urgency = str(urgency).strip().lower()
    if urgency not in URGENCIES:
        raise ValueError("urgency must be low, medium, or high.")
    if isinstance(affected_users, bool) or not isinstance(affected_users, int) or affected_users <= 0:
        raise ValueError("affected_users must be a positive integer.")
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def _next_id(tickets):
    numbers = []
    for ticket in tickets:
        ticket_id = str(ticket.get("id", ""))
        if ticket_id.startswith("T") and ticket_id[1:].isdigit():
            numbers.append(int(ticket_id[1:]))
    return f"T{max(numbers, default=0) + 1:03d}"


def create_ticket(tickets, title, category, urgency, affected_users):
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title must not be blank.")
    category_key = str(category).strip().lower()
    if category_key not in CATEGORIES:
        raise ValueError("category must be Network, Hardware, Software, or Other.")
    urgency_key = str(urgency).strip().lower()
    priority = calculate_priority(urgency_key, affected_users)
    ticket = {
        "id": _next_id(tickets),
        "title": title.strip(),
        "category": CATEGORIES[category_key],
        "urgency": urgency_key,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }
    tickets.append(ticket)
    return deepcopy(ticket)


def get_ticket(tickets, ticket_id):
    wanted = str(ticket_id).strip().upper()
    for ticket in tickets:
        if ticket.get("id", "").upper() == wanted:
            return deepcopy(ticket)
    return None


def list_tickets(tickets):
    return deepcopy(tickets)