#!/bin/bash

arquivos=(P*_joined.tabular)
saida_bacterias="bracken_bacterias.tsv"
saida_fungos="bracken_fungos.tsv"

echo -e "sample\tname\ttaxonomy_id\ttaxonomy_lvl\tnew_est_reads\tfraction_total_reads\ttaxonomy_chain" > $saida_bacterias
echo -e "sample\tname\ttaxonomy_id\ttaxonomy_lvl\tnew_est_reads\tfraction_total_reads\ttaxonomy_chain" > $saida_fungos

for arquivo in "${arquivos[@]}"; do
  amostra=$(echo "$arquivo" | cut -d'_' -f1)

  awk -F'\t' -v sample="$amostra" '{
    for (i=1; i<=NF; i++) {
      if ($i ~ /Fungi/) {
        printf "%s\t%s\t%s\t%s\t%s\t%.5f\t%s\n", sample, $1, $2, $3, $6, $7, $i
        break
      }
    }
  }' "$arquivo" >> $saida_fungos

  awk -F'\t' -v sample="$amostra" '{
    for (i=1; i<=NF; i++) {
      if ($i ~ /Bacteria/) {
        printf "%s\t%s\t%s\t%s\t%s\t%.5f\t%s\n", sample, $1, $2, $3, $6, $7, $i
        break
      }
    }
  }' "$arquivo" >> $saida_bacterias
done

