import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy

# Função para calcular índice de Simpson
def simpson_index(counts):
    proportions = counts / counts.sum()
    return 1 - np.sum(proportions ** 2)

# Função para calcular equidade
def evenness(shannon, richness):
    if richness > 1:
        return shannon / np.log(richness)
    else:
        return 0

# Carregar matriz de abundância
df = pd.read_csv("matriz_fungos.tsv", sep="\t", index_col=0)
df = df.T  # Transpor: amostras nas linhas
df = df.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
df = df[df.sum(axis=1) > 0]  # Remover amostras com soma zero

# Calcular índices ecológicos
results = []
for sample in df.index:
    counts = df.loc[sample]
    richness = (counts > 0).sum()
    shannon = entropy(counts, base=np.e)
    simpson = simpson_index(counts)
    eq = evenness(shannon, richness)
    results.append([richness, shannon, simpson, eq])

# Criar DataFrame com resultados
indices_df = pd.DataFrame(results, columns=["Richness", "Shannon", "Simpson", "Evenness"], index=df.index)
indices_df.to_csv("indices_ecologicos_fungos.tsv", sep="\t")

# Separar dados para gráfico
samples = indices_df.index.tolist()
richness = indices_df["Richness"]
others = indices_df[["Shannon", "Simpson", "Evenness"]]

# Criar gráfico com dois eixos Y
fig, ax1 = plt.subplots(figsize=(10, 6))

# Eixo 1: Richness
ax1.bar(samples, richness, color="skyblue", label="Richness")
ax1.set_ylabel("Richness", color="skyblue", fontsize=12)
ax1.tick_params(axis="y", labelcolor="skyblue")

# Eixo 2: Shannon, Simpson, Evenness
ax2 = ax1.twinx()
width = 0.2
x = range(len(samples))

ax2.bar([i - width for i in x], others["Shannon"], width=width, color="orange", label="Shannon")
ax2.bar(x, others["Simpson"], width=width, color="green", label="Simpson")
ax2.bar([i + width for i in x], others["Evenness"], width=width, color="purple", label="Evenness")
ax2.set_ylabel("Diversity Indices", fontsize=12)

# Estilo e rótulos
ax1.set_xticks(x)
ax1.set_xticklabels(samples)
plt.title("Ecological Indices per Fungal Sample", fontsize=14)

# Legenda combinada
fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)

plt.tight_layout()
plt.savefig("ecological_indices_fungi_dual_axis.png", dpi=300)
plt.show()

