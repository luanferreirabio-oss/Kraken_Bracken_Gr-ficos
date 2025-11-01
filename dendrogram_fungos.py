import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist
import numpy as np

# Load fungal abundance matrix
df = pd.read_csv("matriz_fungos.tsv", sep="\t", index_col=0)

# Transpose: samples as rows
df_t = df.T

# Convert all values to numeric
df_t = df_t.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

# Diagnostic: show total reads per sample
print("Total reads per sample:")
print(df_t.sum(axis=1))

# Remove samples with zero total reads
df_t = df_t[df_t.sum(axis=1) > 0]

# Show remaining samples
print("\nRemaining samples:", df_t.index.tolist())
print("Number of samples:", df_t.shape[0])

# Check if there are at least two samples
if df_t.shape[0] < 2:
    raise ValueError("Not enough valid samples to generate the dendrogram.")

# Compute Bray-Curtis distance matrix
dist_matrix = pdist(df_t.values, metric='braycurtis')

# Check for non-finite values
if not np.isfinite(dist_matrix).all():
    raise ValueError("Distance matrix contains non-finite values.")

# Perform hierarchical clustering
linkage_matrix = linkage(dist_matrix, method='average')

# Plot dendrogram
plt.figure(figsize=(10, 6))
dendrogram(linkage_matrix, labels=df_t.index, leaf_rotation=90)
plt.title("Hierarchical Dendrogram of Fungal Samples", fontsize=14)
plt.xlabel("Samples", fontsize=12)
plt.ylabel("Bray-Curtis Distance", fontsize=12)
plt.tight_layout()

# Save image
plt.savefig("dendrogram_fungi.png", dpi=300)
plt.show()

