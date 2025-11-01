import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carregar matriz de abundância
df = pd.read_csv("matriz_bacterias.tsv", sep="\t", index_col=0)

# Transpor para amostras nas linhas
df_t = df.T

# Converter apenas colunas numéricas e garantir inteiros
df_t = df_t.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

# Definir profundidades de amostragem
max_depth = int(df_t.sum(axis=1).min())
depths = np.linspace(100, max_depth, num=10, dtype=int)

# Função para simular rarefação
def rarefy(counts, depth):
    pool = []
    for i, c in enumerate(counts):
        pool.extend([i] * c)
    if len(pool) < depth:
        return np.nan
    sampled = np.random.choice(pool, depth, replace=False)
    return len(set(sampled))

# Gerar curvas de rarefação
plt.figure(figsize=(10, 6))
for sample in df_t.index:
    counts = df_t.loc[sample].values
    richness = [rarefy(counts, d) for d in depths]
    plt.plot(depths, richness, label=sample)

# Estilo e rótulos
plt.title("Rarefaction Curves of Bacterial Samples", fontsize=14)
plt.xlabel("Number of Sequences", fontsize=12)
plt.ylabel("Observed Species (Richness)", fontsize=12)
plt.legend(title="Samples", fontsize=10)
plt.grid(True)
plt.tight_layout()

# Salvar imagem
plt.savefig("curva_rarefacao_bacterias.png", dpi=300)
plt.show()
