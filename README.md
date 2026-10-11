# CampusFlow

CampusFlow is a Python command-line helpdesk app for creating, prioritizing, assigning, tracking, and reporting campus support tickets.

## Requirements
- Python 3.10 or newer (standard library only)

## Run
From this project folder:
```bash
python main.py
```

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Menu
1. Create ticket
2. List tickets
3. View ticket
4. Assign ticket
5. Change ticket status
6. Show work queue
7. Show reports
8. Save now
0. Exit

Tickets are stored in `data/tickets.json`. The runtime JSON file is intentionally excluded from Git so personal/runtime data is not committed.

## Priority rules
Rules are checked in order:
1. high urgency and 10+ affected users = critical
2. high urgency or 10+ affected users = high
3. medium urgency or 3+ affected users = medium
4. otherwise = low

## Workflow
A ticket must be assigned before moving from `open` to `in_progress`. It can then move to `resolved`. A resolved ticket must be explicitly reopened to `open` before further progress.

## Known limitations
This is a local CLI prototype, not a multi-user network service. It does not implement concurrent-write locking or authentication. Team names, reviewed PR links, and actual AI learning evidence should be added by the fellows; do not invent them.