"""JSON persistence for tickets."""
import json
from pathlib import Path


def load_tickets(path):
    path = Path(path)
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"malformed JSON in {path}: {exc}") from exc
    if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
        raise ValueError(f"invalid ticket data in {path}: expected a JSON list of objects.")
    seen = set()
    for ticket in data:
        ticket_id = ticket.get("id")
        if not isinstance(ticket_id, str) or not ticket_id:
            raise ValueError(f"invalid ticket record in {path}: missing string ID.")
        if ticket_id in seen:
            raise ValueError(f"duplicate ticket ID {ticket_id!r} in {path}.")
        seen.add(ticket_id)
    return data


def save_tickets(path, tickets):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(tickets, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    temporary.replace(path)