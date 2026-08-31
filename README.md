# Inbox-to-Task Router

An autonomous agent that watches a Gmail inbox, classifies incoming emails using
Gemini, and takes action without human intervention:
- **Freelance inquiries** → drafts a personalized proposal reply and saves it to Gmail Drafts
- **Bug reports** → automatically creates a GitHub issue with the details

Built for the Taskmaster track of the All Things Agentic Hackathon.

## Architecture

\`\`\`
[Gmail inbox] --poll--> [Agent]
                            |
                            |--> Gemini 3.5 Flash (classify intent)
                            |
                   +--------+--------+
                   |                 |
          [freelance_inquiry]   [bug_report]
                   |                 |
          Gmail Drafts API     GitHub Issues API
                   |                 |
                   +--------+--------+
                            |
                   Gmail label: agent-handled
\`\`\`

## Tech used

- **Gemini 3.5 Flash** (Gemini API) — intent classification and proposal drafting
- **Python** — Gmail API, GitHub API (PyGithub) integration
- **GitHub Actions** — scheduled deployment (runs every 15 minutes)
- **Google Cloud Run** — configured for deployment (see note below)

## Deployment status

This agent is deployed and running on a schedule via **GitHub Actions**
(see \`.github/workflows/agent.yml\`) — it polls the inbox every 15 minutes with
zero manual intervention.

**Cloud Run**: fully configured (\`Dockerfile\` included, deploy command below)
but deployment was blocked at submission time by a persistent Google Cloud
billing verification error (\`OR_BACR2_59\`) that could not be resolved across
multiple accounts and payment methods before the deadline. The deploy command
is included below as evidence the Cloud infrastructure integration is built
and ready:

\`\`\`bash
gcloud run deploy inbox-task-router \\
  --source . \\
  --region us-central1 \\
  --set-env-vars GEMINI_API_KEY=...,GH_ISSUE_TOKEN=...,TARGET_GH_REPO=... \\
  --min-instances 0 \\
  --max-instances 1 \\
  --no-allow-unauthenticated
\`\`\`

## Setup / spin-up instructions

1. Clone this repo:
   \`\`\`bash
   git clone https://github.com/ChandanaJagadish/inbox-task-router.git
   cd inbox-task-router
   \`\`\`

2. Create a virtual environment and install dependencies:
   \`\`\`bash
   python -m venv venv
   venv\\Scripts\\activate   # Windows
   pip install -r requirements.txt
   \`\`\`

3. Create a \`.env\` file in the project root with:
   \`\`\`
   GEMINI_API_KEY=your-gemini-api-key
   GH_ISSUE_TOKEN=your-github-personal-access-token
   TARGET_GH_REPO=yourusername/yourrepo
   \`\`\`

4. Set up Gmail API access:
   - Enable the Gmail API in Google Cloud Console
   - Create OAuth Desktop credentials, download as \`credentials.json\` into the project root
   - First run will open a browser to authorize access, generating \`token.json\`

5. Run the agent:
   \`\`\`bash
   python agent.py
   \`\`\`

## What I learned

Building this taught me the practical difference between calling an LLM API
directly versus building an actual autonomous agent loop — the routing,
state management (via Gmail labels), and error handling (retrying failed
classifications) matter as much as the classification itself. I also learned
a lot about OAuth flows for headless/scheduled environments and GitHub
Actions as a lightweight, free deployment option for scheduled agents.