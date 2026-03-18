import json
from datetime import datetime

def generate_report(results: list) -> dict:
    successful = [r for r in results if "error" not in r]
    failed     = [r for r in results if "error" in r]

    return {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_repos": len(results),
        "successful": len(successful),
        "failed": len(failed),
        "repositories": successful,
        "errors": failed,
        "summary": {
            "avg_activity_score":   round(sum(r["activity_score"] for r in successful) / len(successful), 2) if successful else 0,
            "avg_complexity_score": round(sum(r["complexity_score"] for r in successful) / len(successful), 2) if successful else 0,
            "beginner_count":     sum(1 for r in successful if r["difficulty"] == "Beginner"),
            "intermediate_count": sum(1 for r in successful if r["difficulty"] == "Intermediate"),
            "advanced_count":     sum(1 for r in successful if r["difficulty"] == "Advanced"),
        }
    }

def print_report(report: dict):
    print("\n" + "="*60)
    print(f"  GITHUB REPOSITORY INTELLIGENCE ANALYZER")
    print(f"  Generated at: {report['generated_at']}")
    print("="*60)
    print(f"  Total repos analyzed : {report['total_repos']}")
    print(f"  Successful           : {report['successful']}")
    print(f"  Failed               : {report['failed']}")
    s = report["summary"]
    print(f"\n  Avg Activity Score   : {s['avg_activity_score']}")
    print(f"  Avg Complexity Score : {s['avg_complexity_score']}")
    print(f"\n  Beginner     : {s['beginner_count']} repos")
    print(f"  Intermediate : {s['intermediate_count']} repos")
    print(f"  Advanced     : {s['advanced_count']} repos")
    print("="*60)
    for repo in report["repositories"]:
        print(f"\n  {repo['repo']} ({repo['difficulty']})")
        print(f"  {repo['url']}")
        print(f"  Stars: {repo['stars']} | Forks: {repo['forks']} | Commits: {repo['commits']}")
        print(f"  Activity: {repo['activity_score']} | Complexity: {repo['complexity_score']}")
        print(f"  Languages: {', '.join(repo['languages'])}")
        print(f"  Last updated: {repo['last_updated']}")
        print("  " + "-"*50)

def save_report(report: dict, filename: str = "report.json"):
    with open(filename, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved to {filename}")