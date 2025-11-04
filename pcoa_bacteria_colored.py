import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, dendrogram

# =========================
# 1. Carregar e preparar os dados
# =========================

df = pd.read_csv("matriz_bacterias.tsv", sep="\t", index_col=0).T
df = df.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
df = df[df.sum(axis=1) > 0]

# =========================
# 2. Normalizações
# =========================

df_tss = df.div(df.sum(axis=1), axis=0)
df_hellinger = np.sqrt(df_tss)

# =========================
# 3. Função para PCoA com PCA (sem título)
# =========================

def plot_pcoa(matrix, filename):
    pca = PCA(n_components=2)
    coords = pca.fit_transform(matrix.values)
    explained = pca.explained_variance_ratio_ * 100
    samples = matrix.index.tolist()
    colors = plt.cm.tab10.colors

    fig, ax = plt.subplots(figsize=(8, 6))
    for i, sample in enumerate(samples):
        x, y = coords[i]
        color = colors[i % len(colors)]
        ax.scatter(x, y, color=color, label=sample, s=60, edgecolor='black')
        ax.text(x + 0.01, y, sample, fontsize=9)
        ellipse = Ellipse((x, y), width=0.08, height=0.05, edgecolor=color,
                          facecolor='none', linestyle='--', linewidth=1.2)
        ax.add_patch(ellipse)

    ax.set_xlabel(f"PCoA1 ({explained[0]:.1f}%)", fontsize=12)
    ax.set_ylabel(f"PCoA2 ({explained[1]:.1f}%)", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='best', fontsize=9)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

# =========================
# 4. Função para Dendrograma (sem título)
# =========================

def plot_dendrogram(matrix, filename):
    dist_matrix = pdist(matrix.values, metric='braycurtis')
    linkage_matrix = linkage(dist_matrix, method='average')
    plt.figure(figsize=(10, 6))
    dendrogram(linkage_matrix, labels=matrix.index, leaf_rotation=90)
    plt.xlabel("Amostras", fontsize=12)
    plt.ylabel("Distância Bray–Curtis", fontsize=12)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

# =========================
# 5. Comparar sensibilidade: distância média Bray–Curtis
# =========================

dist_tss = pdist(df_tss.values, metric='braycurtis')
dist_hellinger = pdist(df_hellinger.values, metric='braycurtis')

media_tss = dist_tss.mean()
media_hellinger = dist_hellinger.mean()

print("📊 Comparação de Sensibilidade - Bray–Curtis")
print(f"Distância média (TSS):      {media_tss:.4f}")
print(f"Distância média (Hellinger): {media_hellinger:.4f}")

if media_hellinger > media_tss:
    print("✅ Hellinger foi mais sensível à variação entre amostras.")
elif media_tss > media_hellinger:
    print("✅ TSS foi mais sensível à variação entre amostras.")
else:
    print("⚖️ Ambas as normalizações tiveram sensibilidade equivalente.")

# =========================
# 6. Gerar gráficos
# =========================

plot_pcoa(df_tss, "pcoa_tss.png")
plot_pcoa(df_hellinger, "pcoa_hellinger.png")
plot_dendrogram(df_tss, "dendrogram_tss.png")
plot_dendrogram(df_hellinger, "dendrogram_hellinger.png")

print("✅ Gráficos gerados sem títulos. Prontos para uso em artigo.")
