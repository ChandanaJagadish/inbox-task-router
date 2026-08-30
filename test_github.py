from github_utils import create_github_issue

url = create_github_issue("Test issue from agent", "This is a test issue created automatically.")
print(url)