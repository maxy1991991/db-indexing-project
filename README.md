# Database Indexing and Clustering Study

## Overview
This project evaluates the impact of realistic PostgreSQL indexing and physical clustering strategies on query performance using a ~100,000-row dataset collected from the GitHub Repository Search API. The goal is to measure **when indexing helps, when it hurts, and why**, using controlled baseline vs indexed vs clustered experiments.

---

## Dataset
- **Source:** GitHub Repository Search API
- **Size:** ~100,000 repositories
- **Schema:**  
  `id, name, full_name, stargazers_count, forks_count, language, created_at, updated_at`
- **Storage:** PostgreSQL

---

## Queries Evaluated
1. **Popular repositories**  
   Repositories with ≥ 5000 stars, ordered by stars
2. **Language filter**  
   All repositories where `language = 'Python'`
3. **Recent repositories**  
   Count of repositories created between `2023-01-01` and `2023-02-01`

---

## Indexing Strategies
- **Partial B-tree index** on `stargazers_count` for popular repositories
- **Covering B-tree index** on `language` with included columns
- **BRIN index** on `created_at`
- **Physical clustering** using `CLUSTER` on the covering index

---

## Methodology
- **Baseline:** Primary key index only
- **Indexed:** Secondary indexes added
- **Clustered:** Table physically reordered using `CLUSTER`
- **Measurement:** `EXPLAIN (ANALYZE, FORMAT JSON)`
- **Metric:** Execution time (ms), execution plan node type

---

## Results Summary

### Baseline vs Indexed

| Query | Baseline (ms) | Indexed (ms) | Speedup | Plan Change |
|-----|--------------|--------------|---------|------------|
| Popular repos | 9.93 | 0.378 | **26.27×** | Seq Scan → Index Scan |
| Language filter | 7.87 | 8.97 | **0.88× (slower)** | Seq Scan → Index Only Scan |
| Recent repos (date range) | 6.43 | 17.58 | **0.37× (slower)** | Seq Scan → Aggregate |

---

### Indexed vs Clustered

| Query | Indexed (ms) | Clustered (ms) | Speedup from Clustering |
|-----|--------------|----------------|-------------------------|
| Popular repos | 0.378 | 0.20 | **1.89×** |
| Language filter | 8.97 | 4.85 | **1.85×** |
| Recent repos (date range) | 17.58 | 13.99 | **1.26×** |

---

## Key Findings

### 1. Partial indexes provide dramatic gains for targeted workloads
The partial index on high-star repositories reduced execution time by over **26×**, demonstrating the effectiveness of indexing only the “hot” subset of data instead of the entire table.

### 2. Covering indexes do not guarantee speedups
Although the language query used an **index-only scan**, it was slightly slower than the baseline due to low selectivity and the overhead of scanning a large portion of the index. This highlights that **index-only ≠ faster by default**.

### 3. BRIN indexes can hurt small-range queries
For the one-month date range, the BRIN index increased execution time. This reflects BRIN’s design tradeoff: it excels at large sequential ranges, not narrow filters on moderately sized tables.

### 4. Physical clustering consistently improved indexed performance
Clustering improved performance across all indexed queries:
- Nearly **2×** improvement for read-heavy workloads
- Noticeable gains even for aggregation queries  
However, clustering does not change query plans and must be maintained, making it a **physical optimization, not a logical one**.

---

## Limitations
- GitHub Search API introduces sampling bias
- Single-node PostgreSQL deployment
- No concurrent workload or write-heavy benchmarking
- BRIN effectiveness limited by table size and data locality

---

## Conclusion
This study shows that indexing is not universally beneficial: performance gains depend heavily on **query selectivity, access patterns, and physical data layout**. Partial indexes and clustering offer substantial improvements for targeted workloads, while low-selectivity and small-range queries can regress despite more sophisticated index usage.

---

## Reproducibility
All ingestion, indexing, benchmarking, and analysis steps are automated and can be reproduced using the scripts in this repository.
