import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar matriz de Bray-Curtis
df = pd.read_csv("braycurtis_bacterias.tsv", sep="\t", index_col=0)

# Criar heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df, annot=True, cmap="viridis", square=True, cbar_kws={"label": "Bray-Curtis Dissimilarity"})

# Títulos e rótulos em inglês
plt.title("Heatmap of Bray-Curtis Dissimilarity Between Bacterial Samples", fontsize=12)
plt.xlabel("Samples")
plt.ylabel("Samples")

# Salvar imagem
plt.tight_layout()
plt.savefig("heatmap_braycurtis_bacteria.png", dpi=300)
plt.show()

