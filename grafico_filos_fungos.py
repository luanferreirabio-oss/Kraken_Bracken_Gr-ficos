import pandas as pd
import matplotlib.pyplot as plt
import os

# Caminho para o arquivo
base_path = "/home/luanferreira/Downloads/Bracken_Corrigidos/Joineds Corrigidos"
file_path = os.path.join(base_path, "bracken_fungos.tsv")

# Carregar o arquivo
df = pd.read_csv(file_path, sep="\t", dtype=str)

# Converter coluna de leitura estimada para inteiro
df["new_est_reads"] = df["new_est_reads"].astype(int)

# Extrair o filo (índice 5 da cadeia taxonômica)
df["Phylum"] = df["taxonomy_chain"].apply(
    lambda x: x.split(";")[5] if isinstance(x, str) and "Fungi" in x and len(x.split(";")) > 5 else "Unclassified"
)

# Verificar se há dados
if df.empty or df["new_est_reads"].sum() == 0:
    print("⚠️ Nenhum dado de leitura fúngica foi encontrado.")
else:
    # Agrupar por amostra e filo
    phyla_abundance = {}
    samples = df["sample"].unique()

    for sample in samples:
        df_sample = df[df["sample"] == sample]
        abundance = df_sample.groupby("Phylum")["new_est_reads"].sum()
        phyla_abundance[sample] = abundance

    # Combinar em um único DataFrame
    df_phyla = pd.DataFrame(phyla_abundance).fillna(0)

    # Normalizar para porcentagem
    df_phyla = df_phyla.apply(lambda x: x / x.sum() * 100)

    # Ordenar filos por abundância total
    df_phyla = df_phyla.loc[df_phyla.sum(axis=1).sort_values(ascending=False).index]

    # Gerar gráfico
    plt.figure(figsize=(12, 7))
    df_phyla.T.plot(kind="bar", stacked=True, colormap="tab20", figsize=(12, 7))

    plt.ylabel("Relative Abundance (%)", fontsize=12)
    plt.xlabel("Samples", fontsize=12)
    plt.title("Relative Abundance of Fungal Phyla per Sample", fontsize=14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", title="Phyla")
    plt.tight_layout()

    # Salvar gráfico
    output_path = os.path.join(base_path, "fungal_phyla_abundance.png")
    plt.savefig(output_path, dpi=300)
    plt.show()
    print(f"✅ Plot saved to: {output_path}")
