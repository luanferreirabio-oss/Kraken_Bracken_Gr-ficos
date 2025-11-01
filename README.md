# Kraken_Bracken_Gráficos

Visualizações gráficas para dados metagenômicos processados com Kraken2 e Bracken.

## 📊 Scripts incluídos

- `heatmap_top20_bacterias.py`: Gera um heatmap de presença/ausência das 20 espécies bacterianas mais abundantes por amostra.
- `heatmap_top20_fungos.py`: Gera um heatmap de presença/ausência das 20 espécies fúngicas mais abundantes por amostra.

## 📁 Estrutura esperada dos arquivos de entrada

Os arquivos `.tsv` devem conter pelo menos as seguintes colunas:

- `sample`: nome da amostra (ex: P1, P2, ...)
- `name`: nome da espécie
- `new_est_reads`: número estimado de leituras

## ▶️ Como executar

```bash
python3 heatmap_top20_bacterias.py
python3 heatmap_top20_fungos.py


Requisitos

    Python 3.8+

    Bibliotecas:

        pandas

        matplotlib

        seaborn

Instale com:pip install pandas matplotlib seaborn


Autor

Luan Ferreira — Projeto de visualização metagenômica com Kraken2 + Bracken
