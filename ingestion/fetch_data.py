import os
import json
import time
import requests
from dotenv import load_dotenv
from models import Repo

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

URL = "https://api.github.com/search/repositories"
OUTFILE = "data/raw/repos.json"

def fetch_pages(query="database", max_pages=10):
    all_repos = {}
    
    for page in range(1, max_pages + 1):
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": 100,
            "page": page
        }

        r = requests.get(URL, headers=HEADERS, params=params)

        if r.status_code == 403:
            print("Rate limited. Sleeping 60s.")
            time.sleep(60)
            continue

        r.raise_for_status()
        items = r.json()["items"]

        for item in items:
            repo = Repo(**item)
            all_repos[repo.id] = repo

        print(f"Page {page}: total unique repos = {len(all_repos)}")
        time.sleep(2)  # polite

    with open(OUTFILE, "w") as f:
        json.dump(
            [r.model_dump() for r in all_repos.values()],
            f,
            indent=2,
            default=str
        )

    print(f"Saved {len(all_repos)} repos to {OUTFILE}")

if __name__ == "__main__":
    fetch_pages()
