import os
from dotenv import load_dotenv
load_dotenv()
from github import Github

def create_github_issue(title, body):
    token = os.environ["GITHUB_TOKEN"]
    repo_name = os.environ["GITHUB_REPO"]
    g = Github(token)
    repo = g.get_repo(repo_name)
    issue = repo.create_issue(title=title, body=body)
    return issue.html_url