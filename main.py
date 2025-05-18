import requests
from argu import get_username

def format_event(event):
    event_type = event.get("type")
    repo_name = event.get("repo", {}).get("name", "Unknown repo")
    payload = event.get("payload", {})

    if event_type == "PushEvent":
        commit_count = len(payload.get("commits", []))
        return f"Pushed {commit_count} commit{'s' if commit_count != 1 else ''} to {repo_name}"
    
    elif event_type == "IssuesEvent":
        action = payload.get("action", "performed an action on")
        return f"{action.capitalize()} an issue in {repo_name}"

    elif event_type == "IssueCommentEvent":
        action = payload.get("action", "commented")
        return f"{action.capitalize()} on an issue in {repo_name}"

    elif event_type == "WatchEvent":
        return f"Starred {repo_name}"

    elif event_type == "CreateEvent":
        ref_type = payload.get("ref_type", "resource")
        return f"Created {ref_type} in {repo_name}"

    elif event_type == "ForkEvent":
        return f"Forked {repo_name}"

    else:
        return f"{event_type} at {repo_name}"

url = get_username()

response = requests.get(url)

if response.status_code == 200:
    events = response.json()

    for event in events:
        
        event_id = event.get("id")
        event_type = event.get("type")
        actor_login = event.get("actor", {}).get("login")
        repo_name = event.get("repo", {}).get("name")
        created_at = event.get("created_at")

        print(format_event(event))
else:
    print(f"Hata: {response.status_code}")
