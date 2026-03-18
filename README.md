# GitHub Repository Intelligence Analyzer

A Python tool that analyzes GitHub repositories and generates 
insights about their activity, complexity, and learning difficulty.

## Live Demo
https://app-analyzer.streamlit.app/

## Features
- Activity Score based on commits, contributors, issues, forks, recency
- Complexity Score based on repo size, languages, contributors
- Automatic classification: Beginner / Intermediate / Advanced
- Handles missing data and API errors gracefully
- Rate limit awareness via GitHub token
- Downloadable JSON report

## Scoring Formula

### Activity Score (0-100)
| Factor | Weight |
|--------|--------|
| Commits | 35% |
| Contributors | 25% |
| Open Issues | 15% |
| Forks | 15% |
| Recency (last push) | 10% |

### Complexity Score (0-100)
| Factor | Weight |
|--------|--------|
| Repo size (KB) | 30% |
| Language diversity | 25% |
| Contributors | 25% |
| License | 10% |
| Wiki + Projects | 10% |

### Difficulty Classification
| Combined Score | Label |
|---------------|-------|
| < 30 | Beginner |
| 30 – 60 | Intermediate |
| > 60 | Advanced |

## Sample Output

| Repo | Activity | Complexity | Difficulty |
|------|----------|------------|------------|
| Webiu | 85.5 | 60.74 | Advanced |
| b0bot | 34.58 | 44.29 | Intermediate |
| Nettacker | 100.0 | 75.9 | Advanced |
| tensorflow | 100.0 | 95.0 | Advanced |
| react | 100.0 | 90.0 | Advanced |

## Installation
```bash
git clone https://github.com/StevenStn/github-analyzer.git
cd github-analyzer
pip install -r requirements.txt
```

## Usage

### Web Interface (Streamlit)
```bash
streamlit run app.py
```

### Command Line
```bash
python analyzer.py
```

## Configuration

Set your GitHub token to avoid rate limiting :
```bash
# Linux/Mac
export GITHUB_TOKEN=your_token_here

# Windows
set GITHUB_TOKEN=your_token_here
```

Or enter it directly in the Streamlit interface.

## Project Structure
```
github-analyzer/
├── analyzer.py       # Main analysis pipeline
├── github_api.py     # GitHub API integration
├── scorer.py         # Scoring formulas
├── report.py         # Report generation
├── app.py            # Streamlit web interface
├── requirements.txt  # Dependencies
└── README.md         # Documentation
```

## Limitations
- GitHub API rate limit: 60 req/hour (unauthenticated), 
  5000 req/hour (with token)
- Commit count estimation uses pagination headers
- Very new repos (< 1 month) may score low on recency

## Built With
- Python 3.x
- Streamlit
- Requests
- Pandas

## Author
Steven Stn — GSoC 2026 Applicant @ C2SI