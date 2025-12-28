CREATE INDEX idx_repos_popular_partial
ON repos (stargazers_count DESC)
WHERE stargazers_count >= 5000;
