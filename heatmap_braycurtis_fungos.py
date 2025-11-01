import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

# Carregar matriz de abundância fúngica
df = pd.read_csv("matriz_fungos.tsv", sep="\t", index_col=0)

# Transpor: amostras nas linhas
df_t = df.T

# Converter para valores numéricos
df_t = df_t.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

# Remover amostras com soma zero
df_t = df_t[df_t.sum(axis=1) > 0]

# Calcular matriz de dissimilaridade Bray-Curtis
dist_matrix = pdist(df_t.values, metric='braycurtis')
dist_square = squareform(dist_matrix)

# Criar DataFrame com rótulos
heatmap_df = pd.DataFrame(dist_square, index=df_t.index, columns=df_t.index)

# Plotar heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(heatmap_df, cmap="YlGnBu", annot=True, fmt=".2f", square=True, linewidths=0.5)
plt.title("Bray-Curtis Dissimilarity Heatmap — Fungal Samples", fontsize=14)
plt.tight_layout()

# Salvar imagem
plt.savefig("heatmap_braycurtis_fungos.png", dpi=300)
plt.show()

