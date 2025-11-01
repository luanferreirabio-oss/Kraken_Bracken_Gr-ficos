#!/bin/bash

arquivos=(P*_joined.tabular)
saida_bacterias="bracken_filos_bacterias.tsv"
saida_fungos="bracken_filos_fungos.tsv"

echo -e "sample\tphylum\tnew_est_reads\tfraction_total_reads" > $saida_bacterias
echo -e "sample\tphylum\tnew_est_reads\tfraction_total_reads" > $saida_fungos

for arquivo in "${arquivos[@]}"; do
  amostra=$(echo "$arquivo" | cut -d'_' -f1)

  # FUNGOS
  awk -F'\t' -v sample="$amostra" '{
    for (i=1; i<=NF; i++) {
      if ($i ~ /Fungi/) {
        split($i, tax, ";")
        if (length(tax) > 5) {
          printf "%s\t%s\t%s\t%.5f\n", sample, tax[6], $6, $7
        }
        break
      }
    }
  }' "$arquivo" >> $saida_fungos

  # BACTÉRIAS
  awk -F'\t' -v sample="$amostra" '{
    for (i=1; i<=NF; i++) {
      if ($i ~ /Bacteria/) {
        split($i, tax, ";")
        if (length(tax) > 3) {
          printf "%s\t%s\t%s\t%.5f\n", sample, tax[4], $6, $7
        }
        break
      }
    }
  }' "$arquivo" >> $saida_bacterias
done

