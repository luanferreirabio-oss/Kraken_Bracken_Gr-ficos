import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load fungal abundance matrix
df = pd.read_csv("matriz_fungos.tsv", sep="\t", index_col=0)

# Transpose: samples as rows
df_t = df.T

# Convert all values to numeric
df_t = df_t.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

# Rarefaction function
def rarefy(counts, depth):
    pool = []
    for i, c in enumerate(counts):
        pool.extend([i] * c)
    if len(pool) < depth:
        return np.nan
    sampled = np.random.choice(pool, depth, replace=False)
    return len(set(sampled))

# Generate rarefaction curves
plt.figure(figsize=(10, 6))
for sample in df_t.index:
    counts = df_t.loc[sample].values
    total = counts.sum()
    if total < 100:
        continue
    depths = np.linspace(100, total, num=10, dtype=int)
    depths = np.unique(depths)
    richness = [rarefy(counts, d) for d in depths]
    valid_depths = [d for d, r in zip(depths, richness) if not np.isnan(r)]
    valid_richness = [r for r in richness if not np.isnan(r)]
    plt.plot(valid_depths, valid_richness, label=sample)

# Labels and style
plt.title("Rarefaction Curves of Fungal Samples", fontsize=14)
plt.xlabel("Number of Sequences", fontsize=12)
plt.ylabel("Observed Species (Richness)", fontsize=12)
plt.legend(title="Samples", fontsize=10)
plt.grid(True)
plt.tight_layout()

# Save image
plt.savefig("rarefaction_curve_fungi.png", dpi=300)
plt.show()

