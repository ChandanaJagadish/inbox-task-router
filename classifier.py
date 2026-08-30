import os
import json
from dotenv import load_dotenv
load_dotenv()
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

CLASSIFY_PROMPT = """You are an email triage assistant. Given the subject and body of an email,
classify its intent and return ONLY valid JSON, no other text, no markdown fences.

Format:
{{"intent": "freelance_inquiry" | "bug_report" | "other", "summary": "one sentence summary"}}

Subject: {subject}
Body: {body}
"""

def classify_email(subject, body):
    prompt = CLASSIFY_PROMPT.format(subject=subject, body=body[:1000])
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"intent": "other", "summary": "Could not parse classification"}