from github_api import fetch_all_data
from scorer import get_score_breakdown

data = fetch_all_data("https://github.com/c2siorg/Webiu")
print("Data fetched:", data)
result = get_score_breakdown(data)

for key, value in result.items():
    print(f"{key:20} : {value}")