import json
import pandas as pd
from sqlalchemy import create_engine, text

ENGINE = create_engine(
    "postgresql+psycopg2://github_user:github_pass@localhost:5432/github_db"
)

QUERIES = {
    "popular_repos": """
        EXPLAIN (ANALYZE, FORMAT JSON)
        SELECT full_name, stargazers_count
        FROM repos
        WHERE stargazers_count >= 5000
        ORDER BY stargazers_count DESC
        LIMIT 20;
    """,
    "language_filter": """
        EXPLAIN (ANALYZE, FORMAT JSON)
        SELECT full_name, stargazers_count
        FROM repos
        WHERE language = 'Python';
    """,
    "recent_repos": """
        EXPLAIN (ANALYZE, FORMAT JSON)
        SELECT COUNT(*)
        FROM repos
        WHERE created_at BETWEEN '2023-01-01' AND '2023-02-01';
    """
}

def extract(plan):
    p = plan[0]["Plan"]
    return {
        "execution_time_ms": p["Actual Total Time"],
        "node_type": p["Node Type"]
    }

rows = []

with ENGINE.connect() as conn:
    for name, q in QUERIES.items():
        plan = conn.execute(text(q)).fetchone()[0]
        r = extract(plan)
        r["query"] = name
        r["phase"] = "baseline"
        rows.append(r)

pd.DataFrame(rows).to_csv("analysis/baseline.csv", index=False)
print(rows)
