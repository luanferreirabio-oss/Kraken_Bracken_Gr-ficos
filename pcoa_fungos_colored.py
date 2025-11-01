import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from matplotlib.patches import Ellipse
import numpy as np
from scipy.spatial.distance import pdist, squareform

# Carregar matriz de abundância fúngica
df = pd.read_csv("matriz_fungos.tsv", sep="\t", index_col=0)
df = df.T  # Amostras nas linhas
df = df.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
df = df[df.sum(axis=1) > 0]

# Calcular matriz de dissimilaridade Bray-Curtis
dist_matrix = pdist(df.values, metric='braycurtis')
dist_square = squareform(dist_matrix)
dist_df = pd.DataFrame(dist_square, index=df.index, columns=df.index)

# Aplicar PCA como aproximação do PCoA
pca = PCA(n_components=2)
coords = pca.fit_transform(dist_df.values)
explained = pca.explained_variance_ratio_ * 100

# Amostras e cores
samples = dist_df.index.tolist()
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

# Função para adicionar elipses individuais
def add_ellipse(ax, x, y, color):
    ellipse = Ellipse((x, y), width=0.08, height=0.05, edgecolor=color,
                      facecolor='none', linestyle='--', linewidth=1.2)
    ax.add_patch(ellipse)

# Criar gráfico
fig, ax = plt.subplots(figsize=(8, 6))
for i, sample in enumerate(samples):
    x, y = coords[i, 0], coords[i, 1]
    ax.scatter(x, y, color=colors[i], label=sample)
    ax.text(x + 0.01, y, sample, fontsize=10)
    add_ellipse(ax, x, y, colors[i])

# Eixos e estilo
ax.set_xlabel(f"PCoA1 ({explained[0]:.1f}% variance)", fontsize=12)
ax.set_ylabel(f"PCoA2 ({explained[1]:.1f}% variance)", fontsize=12)
ax.set_title("PCoA of Fungal Communities (Bray-Curtis)", fontsize=14)
ax.grid(True)
ax.legend()
plt.tight_layout()

# Salvar imagem
plt.savefig("pcoa_fungos_colored.png", dpi=300)
plt.show()

