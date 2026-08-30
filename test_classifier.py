from classifier import classify_email
from dotenv import load_dotenv
load_dotenv()

result = classify_email(
    "Website redesign help needed",
    "Hi, I saw your portfolio and I'm looking for someone to redesign our small business website. What are your rates?"
)
print(result)