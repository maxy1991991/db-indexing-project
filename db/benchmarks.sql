-- Q1: point lookup by primary key
SELECT * FROM repos WHERE id = 28457823;

-- Q2: range query
SELECT COUNT(*) FROM repos
WHERE stargazers_count BETWEEN 1000 AND 5000;

-- Q3: filter + sort
SELECT full_name, stargazers_count
FROM repos
WHERE language = 'Python'
ORDER BY stargazers_count DESC
LIMIT 20;

-- Q4: aggregation
SELECT language, COUNT(*)
FROM repos
GROUP BY language;
