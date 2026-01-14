import base64
from email.utils import parsedate_to_datetime


def parse_message(service, msg_id):
    msg = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="full"
    ).execute()

    headers = msg["payload"]["headers"]
    body = ""

    for h in headers:
        if h["name"] == "From":
            sender = h["value"]
        elif h["name"] == "Subject":
            subject = h["value"]
        elif h["name"] == "Date":
            date = parsedate_to_datetime(h["value"]).isoformat()

    parts = msg["payload"].get("parts", [])
    for part in parts:
        if part["mimeType"] == "text/plain":
            data = part["body"]["data"]
            body = base64.urlsafe_b64decode(data).decode("utf-8")
            break

    return sender, subject, date, body
