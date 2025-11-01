# Kraken_Bracken_Gráficos

Visualizações gráficas para dados metagenômicos processados com Kraken2 e Bracken.

## 📊 Scripts incluídos

- criação de matrizes
- indices ecológicos
- heatmaps
- dendogramas
- pcoas

## 📁 Estrutura esperada dos arquivos de entrada

Os arquivos `.tsv` devem conter pelo menos as seguintes colunas:

- `sample`: nome da amostra (ex: P1, P2, ...)
- `name`: nome da espécie
- `new_est_reads`: número estimado de leituras

## ▶️ Como executar

```bash
python3 nome_do_script.py


Requisitos

    Python 3.8+

    Bibliotecas:

        pandas

        matplotlib

        seaborn

Instale com:pip install pandas matplotlib seaborn


Autor

Luan Ferreira — Projeto de visualização metagenômica com Kraken2 + Bracken
