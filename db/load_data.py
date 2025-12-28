import json
from sqlalchemy import create_engine, text

ENGINE = create_engine(
    "postgresql+psycopg2://github_user:github_pass@localhost:5432/github_db"
)

with open("data/raw/repos.json") as f:
    repos = json.load(f)

with ENGINE.begin() as conn:
    for r in repos:
        conn.execute(
            text("""
                INSERT INTO repos (
                    id, name, full_name,
                    stargazers_count, forks_count,
                    language, created_at, updated_at
                )
                VALUES (
                    :id, :name, :full_name,
                    :stargazers_count, :forks_count,
                    :language, :created_at, :updated_at
                )
                ON CONFLICT (id) DO NOTHING
            """),
            r
        )

print(f"Inserted {len(repos)} repos")
