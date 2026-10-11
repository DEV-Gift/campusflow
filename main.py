"""CampusFlow command-line helpdesk application."""
from pathlib import Path

from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket, get_ticket, list_tickets
from campusflow.workflow import assign_ticket, change_status, work_queue
from campusflow.reports import build_report, print_report

DATA_FILE = Path("data/tickets.json")


def prompt_non_empty(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("Error: this field cannot be blank.")


def create_from_input(tickets):
    title = prompt_non_empty("Title: ")
    category = input("Category (Network/Hardware/Software/Other): ").strip()
    urgency = input("Urgency (low/medium/high): ").strip()
    while True:
        raw_users = input("Number of affected users: ").strip()
        try:
            affected_users = int(raw_users)
            break
        except ValueError:
            print("Error: affected users must be a positive whole number.")
    ticket = create_ticket(tickets, title, category, urgency, affected_users)
    print(f"Created {ticket['id']} with {ticket['priority']} priority.")


def show_ticket(ticket):
    if not ticket:
        print("Ticket not found.")
        return
    for key, value in ticket.items():
        print(f"{key}: {value}")


def main():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        tickets = load_tickets(DATA_FILE)
    except ValueError as exc:
        print(f"Cannot start safely: {exc}")
        print("Fix or restore data/tickets.json before restarting.")
        return

    actions = {
        "1": "Create ticket",
        "2": "List tickets",
        "3": "View ticket",
        "4": "Assign ticket",
        "5": "Change ticket status",
        "6": "Show work queue",
        "7": "Show reports",
        "8": "Save now",
        "0": "Exit",
    }
    while True:
        print("\n=== CampusFlow ===")
        for key, label in actions.items():
            print(f"{key}. {label}")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                create_from_input(tickets)
                save_tickets(DATA_FILE, tickets)
            elif choice == "2":
                for ticket in list_tickets(tickets):
                    print("-" * 30)
                    show_ticket(ticket)
                if not tickets:
                    print("No tickets yet.")
            elif choice == "3":
                show_ticket(get_ticket(tickets, input("Ticket ID: ")))
            elif choice == "4":
                tid = input("Ticket ID: ")
                staff = prompt_non_empty("Staff member: ")
                assign_ticket(tickets, tid, staff)
                save_tickets(DATA_FILE, tickets)
                print("Ticket assigned.")
            elif choice == "5":
                tid = input("Ticket ID: ")
                status = input("New status (open/in_progress/resolved): ")
                change_status(tickets, tid, status)
                save_tickets(DATA_FILE, tickets)
                print("Ticket status updated.")
            elif choice == "6":
                queue = work_queue(tickets)
                if not queue:
                    print("No unresolved tickets.")
                for ticket in queue:
                    print(f"{ticket['id']} [{ticket['priority']}] {ticket['status']} - {ticket['title']}")
            elif choice == "7":
                print_report(build_report(tickets))
            elif choice == "8":
                save_tickets(DATA_FILE, tickets)
                print("Saved.")
            elif choice == "0":
                save_tickets(DATA_FILE, tickets)
                print("Goodbye.")
                break
            else:
                print("Choose one of the listed options.")
        except (ValueError, KeyError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()