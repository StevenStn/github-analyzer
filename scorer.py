from datetime import datetime, timezone

def calculate_activity_score(data: dict) -> float:
    """
    Activity Score (0-100) basé sur :
    - Commits      : 35%
    - Contributors : 25%
    - Open Issues  : 15%
    - Forks        : 15%
    - Recence      : 10% (date du dernier push)
    """
    if not data or "error" in data:
        return 0.0

    # Normalisation avec des plafonds raisonnables
    commits_score     = min(data.get("commits", 0) / 1000, 1.0) * 35
    contributors_score = min(data.get("contributors", 0) / 50, 1.0) * 25
    issues_score      = min(data.get("open_issues", 0) / 100, 1.0) * 15
    forks_score       = min(data.get("forks", 0) / 200, 1.0) * 15

    # Récence : score plein si mis à jour dans les 30 derniers jours
    recency_score = 0.0
    updated_at = data.get("updated_at", "")
    if updated_at:
        try:
            last_update = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            days_since = (datetime.now(timezone.utc) - last_update).days
            recency_score = max(0.0, 1.0 - (days_since / 365)) * 10
        except:
            pass

    total = commits_score + contributors_score + issues_score + forks_score + recency_score
    return round(total, 2)


def calculate_complexity_score(data: dict) -> float:
    """
    Complexity Score (0-100) basé sur :
    - Taille du repo (KB)  : 30%
    - Nb de langages       : 25%
    - Nb de contributors   : 25%
    - A une licence        : 10%
    - Wiki + Projects      : 10%
    """
    if not data or "error" in data:
        return 0.0

    size_score        = min(data.get("size", 0) / 50000, 1.0) * 30
    languages_score   = min(len(data.get("languages", {})) / 5, 1.0) * 25
    contributors_score = min(data.get("contributors", 0) / 50, 1.0) * 25
    license_score     = 10.0 if data.get("license", "None") != "None" else 0.0
    extras_score      = (5.0 if data.get("has_wiki") else 0.0) + \
                        (5.0 if data.get("has_projects") else 0.0)

    total = size_score + languages_score + contributors_score + license_score + extras_score
    return round(total, 2)


def classify_difficulty(activity: float, complexity: float) -> str:
    """
    Classification basée sur la combinaison des deux scores.
    """
    combined = (activity * 0.5) + (complexity * 0.5)

    if combined < 30:
        return "Beginner"
    elif combined < 60:
        return "Intermediate"
    else:
        return "Advanced"


def get_score_breakdown(data: dict) -> dict:
    """
    Retourne tous les scores + classification pour un repo.
    """
    activity   = calculate_activity_score(data)
    complexity = calculate_complexity_score(data)
    difficulty = classify_difficulty(activity, complexity)

    return {
        "repo":        data.get("name", "Unknown"),
        "url":         data.get("url", ""),
        "description": data.get("description", "")[:150] + "..." if len(data.get("description") or "") > 150 else data.get("description", ""),
        "stars":       data.get("stars", 0),
        "forks":       data.get("forks", 0),
        "commits":     data.get("commits", 0),
        "contributors": data.get("contributors", 0),
        "languages":   list(data.get("languages", {}).keys()),
        "activity_score":   activity,
        "complexity_score": complexity,
        "difficulty":       difficulty,
        "last_updated": data.get("updated_at", "")[:10],
    }