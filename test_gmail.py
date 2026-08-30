from gmail_utils import get_gmail_service, get_unread_messages, extract_subject_and_body
from dotenv import load_dotenv
load_dotenv()

service = get_gmail_service()
messages = get_unread_messages(service)
print(f"Found {len(messages)} unread message(s).")
for m in messages:
    subject, sender, body = extract_subject_and_body(m)
    print(f"From: {sender}")
    print(f"Subject: {subject}")
    print(f"Body preview: {body[:150]}")
    print("---")