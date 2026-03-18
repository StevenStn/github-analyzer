import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else "",
    "Accept": "application/vnd.github.v3+json"
}

def get_repo_data(owner: str, repo: str) -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return {}
    return response.json()

def get_commits_count(owner: str, repo: str) -> int:
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=1"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return 0
    link = response.headers.get("Link", "")
    if 'rel="last"' in link:
        try:
            last_url = [l.strip() for l in link.split(",") if 'rel="last"' in l][0]
            last_page = int(last_url.split("page=")[-1].split(">")[0])
            return last_page
        except:
            return 1
    return len(response.json())

def get_contributors_count(owner: str, repo: str) -> int:
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=1&anon=true"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return 0
    link = response.headers.get("Link", "")
    if 'rel="last"' in link:
        try:
            last_url = [l.strip() for l in link.split(",") if 'rel="last"' in l][0]
            last_page = int(last_url.split("page=")[-1].split(">")[0])
            return last_page
        except:
            return 1
    return len(response.json())

def get_languages(owner: str, repo: str) -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return {}
    return response.json()

def get_open_issues_count(owner: str, repo: str) -> int:
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=open&per_page=1"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return 0
    link = response.headers.get("Link", "")
    if 'rel="last"' in link:
        try:
            last_url = [l.strip() for l in link.split(",") if 'rel="last"' in l][0]
            last_page = int(last_url.split("page=")[-1].split(">")[0])
            return last_page
        except:
            return 1
    return len(response.json())

def parse_repo_url(url: str) -> tuple:
    parts = url.rstrip("/").split("/")
    if len(parts) >= 2:
        return parts[-2], parts[-1]
    return None, None

def fetch_all_data(repo_url: str) -> dict:
    owner, repo = parse_repo_url(repo_url)
    if not owner or not repo:
        return {"error": f"Invalid URL: {repo_url}"}

    print(f"Fetching data for {owner}/{repo}...")
    base = get_repo_data(owner, repo)
    if not base:
        return {"error": f"Cannot fetch repo: {repo_url}"}

    return {
        "url": repo_url,
        "name": base.get("name", repo),
        "description": base.get("description", ""),
        "stars": base.get("stargazers_count", 0),
        "forks": base.get("forks_count", 0),
        "open_issues": base.get("open_issues_count", 0),
        "watchers": base.get("watchers_count", 0),
        "size": base.get("size", 0),
        "created_at": base.get("created_at", ""),
        "updated_at": base.get("pushed_at", ""),
        "default_branch": base.get("default_branch", "main"),
        "has_wiki": base.get("has_wiki", False),
        "has_projects": base.get("has_projects", False),
        "license": base.get("license", {}).get("name", "None") if base.get("license") else "None",
        "commits": get_commits_count(owner, repo),
        "contributors": get_contributors_count(owner, repo),
        "languages": get_languages(owner, repo),
    }