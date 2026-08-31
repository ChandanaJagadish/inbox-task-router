from gmail_utils import get_gmail_service, get_unread_messages
from agent import process_email

def run_once():
    service = get_gmail_service()
    messages = get_unread_messages(service)
    if not messages:
        print("No new unread messages.")
    for message in messages:
        process_email(service, message)

if __name__ == "__main__":
    run_once()