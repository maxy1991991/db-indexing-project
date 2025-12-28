## Conclusions

- **Primary key lookups were already as good as they get.**  
  Queries that filter by `id` used the primary key index both before and after adding new indexes. The faster runtime observed later is best explained by caching effects rather than any real change in query strategy. In other words, PostgreSQL was already doing the right thing here.

- **Range indexes don’t always help—especially on small tables.**  
  The `stargazers_count BETWEEN …` query continued to use a sequential scan even after an index was added. This makes sense: most rows matched the condition, and the table is small enough that scanning everything is cheaper than bouncing through an index. This is a good reminder that indexes are not automatically beneficial.

- **The biggest win came from matching the index to the query pattern.**  
  For the query filtering by `language` and ordering by `stargazers_count` with a `LIMIT`, indexing made a clear difference. PostgreSQL switched from scanning the table and sorting the results to scanning the index in reverse order and stopping early. This reduced execution time by about an order of magnitude.

- **Indexes influence *how* queries run, not just *how fast*.**  
  The most important change wasn’t just lower latency, but a completely different execution plan. Once the index matched the filter and sort order, PostgreSQL no longer needed to sort at all. This highlights why index design should be driven by actual access patterns, not guesswork.

**Takeaway:** Indexes are most effective when they reflect how queries filter, order, and limit data. Adding indexes indiscriminately often has little effect, but aligning them with real workloads can produce dramatic improvements.
