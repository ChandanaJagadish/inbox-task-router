from gmail_utils import get_gmail_service, create_draft_reply
from proposal import draft_proposal

service = get_gmail_service()

subject = "Website redesign help needed"
body = "Hi, I saw your portfolio and I'm looking for someone to redesign our small business website. What are your rates?"

proposal_text = draft_proposal(subject, body)
create_draft_reply(service, "test@example.com", subject, proposal_text)
print("Draft created! Check your Gmail Drafts folder.")