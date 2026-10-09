# Design decisions

- Tickets are stored as a list of dictionaries so they can be serialized directly to JSON.
- `tickets.py` owns validation, ID generation, lookup, and the priority rules.
- `workflow.py` owns assignment, status transitions, and queue ordering.
- `storage.py` owns JSON loading and saving.
- Business logic functions are separate from interactive input so unit tests can call them directly.
- Invalid operations raise `ValueError`; the CLI catches and displays these messages.
- Queue ordering is priority rank first, then numeric ticket ID.
- JSON is written to a temporary file and then replaced to reduce the chance of a partial write.