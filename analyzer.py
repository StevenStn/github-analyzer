from github_api import fetch_all_data
from scorer import get_score_breakdown
from report import generate_report, print_report, save_report

REPOS = [
    "https://github.com/c2siorg/Webiu",
    "https://github.com/c2siorg/b0bot",
    "https://github.com/OWASP/Nettacker",
    "https://github.com/tensorflow/tensorflow",
    "https://github.com/facebook/react",
]

def analyze(repo_urls: list) -> dict:
    results = []
    for url in repo_urls:
        data = fetch_all_data(url)
        score = get_score_breakdown(data)
        results.append(score)
    return generate_report(results)

if __name__ == "__main__":
    report = analyze(REPOS)
    print_report(report)
    save_report(report)