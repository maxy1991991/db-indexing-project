CREATE TABLE repos (
    id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    full_name TEXT NOT NULL,
    stargazers_count INT,
    forks_count INT,
    language TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
