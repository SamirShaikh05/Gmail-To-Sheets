import json
import os
from gmail_service import get_gmail_service, fetch_unread_messages, mark_as_read
from sheets_service import get_sheets_service, append_row
from email_parser import parse_message
from config import STATE_FILE


def load_state():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, "r") as f:
        return set(json.load(f))


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(list(state), f)


def main():
    gmail = get_gmail_service()
    sheets = get_sheets_service()

    processed = load_state()
    messages = fetch_unread_messages(gmail)

    for msg in messages:
        if msg["id"] in processed:
            continue

        sender, subject, date, body = parse_message(gmail, msg["id"])
        append_row(sheets, [sender, subject, date, body])
        mark_as_read(gmail, msg["id"])

        processed.add(msg["id"])

    save_state(processed)


if __name__ == "__main__":
    main()
