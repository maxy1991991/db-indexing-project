import json
import pandas as pd
from sqlalchemy import create_engine, text

ENGINE = create_engine(
    "postgresql+psycopg2://github_user:github_pass@localhost:5432/github_db"
)

QUERIES = {
    "popular_repos": """
        EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
        SELECT full_name, stargazers_count
        FROM repos
        WHERE stargazers_count >= 5000
        ORDER BY stargazers_count DESC
        LIMIT 20;
    """,
    "language_filter": """
        EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
        SELECT full_name, stargazers_count
        FROM repos
        WHERE language = 'Python';
    """,
    "recent_repos": """
        EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
        SELECT COUNT(*)
        FROM repos
        WHERE created_at >= '2022-01-01';
    """
}


def extract_metrics(plan):
    plan = plan[0]["Plan"]
    return {
        "execution_time_ms": plan["Actual Total Time"],
        "node_type": plan["Node Type"],
        "rows": plan.get("Actual Rows", None)
    }

results = []

with ENGINE.connect() as conn:
    for name, sql in QUERIES.items():
        result = conn.execute(text(sql)).fetchone()[0]
        metrics = extract_metrics(result)
        metrics["query"] = name
        metrics["phase"] = "indexed"
        results.append(metrics)

df = pd.DataFrame(results)
df.to_csv("analysis/results.csv", index=False)

print(df)
