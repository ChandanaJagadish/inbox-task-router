import os
from dotenv import load_dotenv
load_dotenv()
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Fill this in with 2-3 of your own real projects — this is what Gemini
# will reference when writing a proposal reply
MY_PROJECTS = """
- Built a Django-based crop prediction app using ML models for agricultural forecasting
- Built a full-stack AI tutoring platform (React + Vite, FastAPI, Gemini API)
- Built a text-to-video generation tool
"""

PROPOSAL_PROMPT = """Write a short, friendly, professional proposal email reply (under 150 words)
to a potential freelance client. Reference 1-2 relevant past projects naturally if they fit.
Do not invent pricing — say you'll follow up with a quote after a quick call.

My past projects:
{projects}

Their email:
Subject: {subject}
Body: {body}
"""

def draft_proposal(subject, body):
    prompt = PROPOSAL_PROMPT.format(projects=MY_PROJECTS, subject=subject, body=body[:1000])
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    return response.text.strip()