"""Ticket reporting."""
from collections import Counter


def build_report(tickets):
    statuses = Counter(ticket.get("status", "unknown") for ticket in tickets)
    priorities = Counter(ticket.get("priority", "unknown") for ticket in tickets)
    return {
        "total": len(tickets),
        "by_status": {key: statuses.get(key, 0) for key in ("open", "in_progress", "resolved")},
        "by_priority": {key: priorities.get(key, 0) for key in ("critical", "high", "medium", "low")},
    }


def print_report(report):
    print(f"Total tickets: {report['total']}")
    print("By status:")
    for key, count in report["by_status"].items():
        print(f"  {key}: {count}")
    print("By priority:")
    for key, count in report["by_priority"].items():
        print(f"  {key}: {count}")