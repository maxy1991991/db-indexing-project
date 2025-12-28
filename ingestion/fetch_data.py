import os
import json
import time
import requests
from datetime import date, timedelta
from dotenv import load_dotenv
from models import Repo
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

URL = "https://api.github.com/search/repositories"
OUTFILE = "data/raw/repos.json"
PROGRESS_FILE = "ingestion/progress.json"

START_DATE = date(2015, 1, 1)
END_DATE = date(2024, 1, 1)
WINDOW_DAYS = 30
PER_PAGE = 100
MAX_PAGES = 10

# ---------- HTTP session with retries ----------
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[500, 502, 503, 504],
)
session.mount("https://", HTTPAdapter(max_retries=retries))

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            p = json.load(f)
            return date.fromisoformat(p["start_date"]), p["page"]
    return START_DATE, 1

def save_progress(start_date, page):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(
            {"start_date": start_date.isoformat(), "page": page},
            f
        )

def date_windows(start, end, step):
    cur = start
    while cur < end:
        nxt = min(cur + timedelta(days=step), end)
        yield cur, nxt
        cur = nxt

def fetch_window(start_date, end_date, start_page, all_repos):
    query = f"created:{start_date}..{end_date}"

    for page in range(start_page, MAX_PAGES + 1):
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": PER_PAGE,
            "page": page
        }

        try:
            r = session.get(
                URL,
                headers=HEADERS,
                params=params,
                timeout=10
            )
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"Network error on {start_date} page {page}: {e}")
            save_progress(start_date, page)
            raise

        items = r.json().get("items", [])
        if not items:
            break

        for item in items:
            repo = Repo(**item)
            all_repos[repo.id] = repo

        print(
            f"{start_date} → {end_date} | page {page} | total {len(all_repos)}"
        )

        save_progress(start_date, page + 1)
        time.sleep(2)

def main():
    all_repos = {}

    if os.path.exists(OUTFILE):
        with open(OUTFILE) as f:
            for r in json.load(f):
                all_repos[r["id"]] = Repo(**r)

    resume_date, resume_page = load_progress()
    resumed = False

    for start, end in date_windows(START_DATE, END_DATE, WINDOW_DAYS):
        if start < resume_date:
            continue

        page = resume_page if not resumed else 1
        resumed = True

        fetch_window(start, end, page, all_repos)

        with open(OUTFILE, "w") as f:
            json.dump(
                [r.model_dump() for r in all_repos.values()],
                f,
                indent=2,
                default=str
            )

        save_progress(end, 1)

    print(f"Final total repos: {len(all_repos)}")

if __name__ == "__main__":
    main()
