import pandas as pd

no_cluster = pd.read_csv("analysis/indexed_no_cluster.csv")
clustered = pd.read_csv("analysis/indexed_clustered.csv")

df = no_cluster.merge(
    clustered,
    on="query",
    suffixes=("_no_cluster", "_clustered")
)

df["speedup_from_clustering"] = (
    df["execution_time_ms_no_cluster"] /
    df["execution_time_ms_clustered"]
)

df.to_csv("analysis/clustering_comparison.csv", index=False)
print(df)
