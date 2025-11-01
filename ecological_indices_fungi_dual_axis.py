import pandas as pd
import matplotlib.pyplot as plt

# Carregar os índices ecológicos dos fungos
df = pd.read_csv("indices_ecologicos_fungos.tsv", sep="\t", index_col=0)

# Renomear colunas para inglês
df = df.rename(columns={
    "Riqueza": "Richness",
    "Shannon": "Shannon",
    "Simpson": "Simpson",
    "Equidade": "Evenness"
})

# Separar os dados
samples = df.index.tolist()
richness = df["Richness"]
others = df[["Shannon", "Simpson", "Evenness"]]

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

