import pandas as pd
import numpy as np
from scipy.stats import entropy
from skbio.diversity import beta_diversity

# Carregar matriz
df = pd.read_csv("matriz_bacterias.tsv", sep="\t", index_col=0)
df = df.apply(pd.to_numeric, errors="coerce")

# Filtrar espécies com <10 reads totais ou presentes em <2 amostras
df_filtrada = df[(df.sum(axis=1) >= 10) & (df.astype(bool).sum(axis=1) >= 2)]

# Normalizar por amostra (abundância relativa)
df_normalizada = df_filtrada.div(df_filtrada.sum(axis=0), axis=1)

# Calcular Bray-Curtis
bray = beta_diversity("braycurtis", df_normalizada.T.values, ids=df_normalizada.columns)
matriz_bray = pd.DataFrame(bray.data, index=bray.ids, columns=bray.ids)
matriz_bray.to_csv("braycurtis_bacterias.tsv", sep="\t")

# Calcular índices ecológicos
def calcular_indices(coluna):
    abundancias = coluna[coluna > 0]
    total = abundancias.sum()
    rel_abund = abundancias / total
    riqueza = len(abundancias)
    shannon = entropy(rel_abund, base=np.e)
    simpson = 1 - sum(rel_abund**2)
    equidade = shannon / np.log(riqueza) if riqueza > 1 else 0
    return pd.Series([riqueza, shannon, simpson, equidade], index=["Riqueza", "Shannon", "Simpson", "Equidade"])

indices = df_filtrada.apply(calcular_indices, axis=0)
indices.T.to_csv("indices_ecologicos_bacterias.tsv", sep="\t")
