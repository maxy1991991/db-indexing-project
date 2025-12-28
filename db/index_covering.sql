CREATE INDEX idx_repos_language_cover
ON repos (language)
INCLUDE (full_name, stargazers_count);
