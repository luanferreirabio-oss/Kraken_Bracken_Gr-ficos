import pandas as pd
import matplotlib.pyplot as plt
import os

# Path to input files
base_path = "/home/luanferreira/Downloads/Bracken_Corrigidos/Joineds Corrigidos"

# Sample identifiers
samples = ["P1", "P2", "P3", "P4", "P5", "P6"]
phyla_abundance = {}

# Process each sample file
for sample in samples:
    file_path = os.path.join(base_path, f"{sample}_joined.tabular")
    try:
        df = pd.read_csv(file_path, sep="\t", header=0, low_memory=False)

        # Identify taxonomy column (contains hierarchical lineage)
        tax_col = [col for col in df.columns if df[col].astype(str).str.contains("cellular organisms;Bacteria").any()]
        if tax_col:
            tax_column = tax_col[0]
        else:
            print(f"[{sample}] Taxonomy column not found.")
            continue

        # Extract phylum (4th level in taxonomy string)
        df["Phylum"] = df[tax_column].apply(lambda x: x.split(";")[3] if isinstance(x, str) and len(x.split(";")) > 3 else "Unclassified")

        # Check if abundance column exists
        if "fraction_total_reads" not in df.columns:
            print(f"[{sample}] 'fraction_total_reads' column missing.")
            continue

        # Sum relative abundance per phylum
        abundance = df.groupby("Phylum")["fraction_total_reads"].sum()
        phyla_abundance[sample] = abundance

    except Exception as e:
        print(f"[{sample}] Error processing file: {e}")

# Combine data into a single DataFrame
df_phyla = pd.DataFrame(phyla_abundance).fillna(0)

if df_phyla.empty:
    print("No abundance data was processed.")
else:
    # Normalize to percentage
    df_phyla = df_phyla.apply(lambda x: x / x.sum() * 100)

    # Sort phyla by total abundance
    df_phyla = df_phyla.loc[df_phyla.sum(axis=1).sort_values(ascending=False).index]

    # Generate stacked bar plot
    plt.figure(figsize=(12, 7))
    df_phyla.T.plot(kind="bar", stacked=True, colormap="tab20", figsize=(12, 7))

    plt.ylabel("Relative Abundance (%)", fontsize=12)
    plt.xlabel("Samples", fontsize=12)
    plt.title("Relative Abundance of Bacterial Phyla per Sample", fontsize=14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", title="Phyla")
    plt.tight_layout()

    # Save plot
    output_path = os.path.join(base_path, "bacterial_phyla_abundance.png")
    plt.savefig(output_path, dpi=300)
    plt.show()
    print(f"✅ Plot saved to: {output_path}")
