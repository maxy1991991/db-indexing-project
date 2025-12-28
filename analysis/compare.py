import pandas as pd

base = pd.read_csv("analysis/baseline.csv")
idx = pd.read_csv("analysis/indexed_no_cluster.csv")

df = base.merge(idx, on="query", suffixes=("_baseline", "_indexed"))

df["speedup"] = (
    df["execution_time_ms_baseline"] /
    df["execution_time_ms_indexed"]
)

df.to_csv("analysis/comparison.csv", index=False)
print(df)
