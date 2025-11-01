import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Caminho para o arquivo
base_path = "/home/luanferreira/Downloads/Bracken_Corrigidos/Joineds Corrigidos"
fungi_file = os.path.join(base_path, "bracken_fungos.tsv")

# Carregar os dados
df = pd.read_csv(fungi_file, sep="\t", dtype=str)

# Limpar nomes de espécies
df["name"] = df["name"].str.strip().str.lower()

# Remover linhas onde 'new_est_reads' não é numérico
df = df[df["new_est_reads"].str.replace(",", "").str.isnumeric()]

# Converter para inteiro
df["new_est_reads"] = df["new_est_reads"].str.replace(",", "").astype(int)

# Somar abundância total por espécie
top_species = df.groupby("name")["new_est_reads"].sum().sort_values(ascending=False).head(20).index.tolist()

# Filtrar apenas as 20 espécies mais abundantes
df_top = df[df["name"].isin(top_species)]

# Criar matriz de presença/ausência
presence_matrix = pd.crosstab(df_top["name"], df_top["sample"])
presence_matrix = presence_matrix.applymap(lambda x: 1 if x > 0 else 0)

# Ordenar espécies por total de presença
presence_matrix["total"] = presence_matrix.sum(axis=1)
presence_matrix = presence_matrix.sort_values("total", ascending=False).drop(columns="total")

# Gerar heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(presence_matrix, cmap="Purples", linewidths=0.5, linecolor="gray", cbar=False)

plt.title("Presence/Absence of Top 20 Fungal Species per Sample", fontsize=14)
plt.xlabel("Samples", fontsize=12)
plt.ylabel("Fungal Species", fontsize=12)
plt.tight_layout()

# Salvar gráfico
output_path = os.path.join(base_path, "heatmap_top20_fungal_species.png")
plt.savefig(output_path, dpi=300)
plt.show()
print(f"✅ Heatmap salvo em: {output_path}")

