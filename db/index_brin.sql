CREATE INDEX idx_repos_created_brin
ON repos USING BRIN (created_at);
