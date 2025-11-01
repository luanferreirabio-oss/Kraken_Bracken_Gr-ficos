import pandas as pd

def gerar_matriz(caminho_entrada, caminho_saida):
    df = pd.read_csv(caminho_entrada, sep="\t")
    matriz = df.pivot_table(index="name", columns="sample", values="new_est_reads", aggfunc="sum").fillna(0)
    matriz.to_csv(caminho_saida, sep="\t")

# Gerar matriz para bactérias
gerar_matriz("bracken_bacterias.tsv", "matriz_bacterias.tsv")

# Gerar matriz para fungos
gerar_matriz("bracken_fungos.tsv", "matriz_fungos.tsv")

