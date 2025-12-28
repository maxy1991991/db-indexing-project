import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

baseline = pd.read_csv("analysis/baseline.csv")
indexed = pd.read_csv("analysis/indexed.csv")
clustered = pd.read_csv("analysis/indexed_clustered.csv")

# Map query → index type
INDEX_LABEL = {
    "popular_repos": "Partial index",
    "language_filter": "Covering index",
    "recent_repos": "BRIN index"
}

# Merge all phases
df = baseline.merge(
    indexed,
    on="query",
    suffixes=("_baseline", "_indexed")
).merge(
    clustered,
    on="query"
)

df.rename(
    columns={"execution_time_ms": "execution_time_ms_clustered"},
    inplace=True
)

x = np.arange(len(df))
width = 0.25

plt.figure(figsize=(9, 5))

# Baseline bars
plt.bar(
    x - width,
    df["execution_time_ms_baseline"],
    width,
    label="Baseline"
)

# Indexed bars (label differs per query, but bar position is shared)
plt.bar(
    x,
    df["execution_time_ms_indexed"],
    width,
    label="Indexed (query-specific)"
)

# Clustered bars
plt.bar(
    x + width,
    df["execution_time_ms_clustered"],
    width,
    label="Clustered"
)

# X labels
plt.xticks(
    x,
    [
        f"{q}\n({INDEX_LABEL[q]})"
        for q in df["query"]
    ]
)

plt.ylabel("Execution Time (ms)")
plt.title("Baseline vs Index Type vs Clustered Performance")
plt.legend()
plt.tight_layout()
plt.savefig("analysis/performance.png")
plt.close()
