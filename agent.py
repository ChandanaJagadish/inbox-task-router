import time
from gmail_utils import (
    get_gmail_service, get_unread_messages,
    extract_subject_and_body, create_draft_reply, label_as_handled
)
from classifier import classify_email
from proposal import draft_proposal
from github_utils import create_github_issue

def process_email(service, message):
    subject, sender, body = extract_subject_and_body(message)

    try:
        result = classify_email(subject, body)
    except Exception as e:
        print(f"  -> Classification failed, will retry next cycle: {e}")
        return  # skip this email for now, don't label it, try again next loop

    intent = result.get("intent", "other")
    summary = result.get("summary", "")

    print(f"[{intent}] {subject} — {summary}")

    try:
        if intent == "freelance_inquiry":
            proposal_text = draft_proposal(subject, body)
            create_draft_reply(service, sender, subject, proposal_text)
            print("  -> Draft reply created in Gmail")

        elif intent == "bug_report":
            issue_url = create_github_issue(
                title=f"[From email] {subject}",
                body=f"Reported via email from {sender}\n\nSummary: {summary}\n\nOriginal body:\n{body[:500]}"
            )
            print(f"  -> GitHub issue created: {issue_url}")

        else:
            print("  -> No action taken (intent: other)")

        label_as_handled(service, message["id"])

    except Exception as e:
        print(f"  -> Action failed, will retry next cycle: {e}")



def run_loop(poll_seconds=60):
    service = get_gmail_service()
    print(f"Agent started. Watching inbox every {poll_seconds} seconds. Ctrl+C to stop.")
    while True:
        messages = get_unread_messages(service)
        if not messages:
            print("No new unread messages.")
        for message in messages:
            process_email(service, message)
        time.sleep(poll_seconds)


if __name__ == "__main__":
    run_loop()