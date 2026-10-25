# Desafio Citi — Engenharia de Dados

## Sobre o projeto

Neste projeto realizei o tratamento e a transformação dos dados a partir de uma planilha, organizando o processamento em camadas Bronze, Silver e Gold.

## Estrutura do projeto

```text
desafio_citi_dados/
├── data/
│   ├── brutos/
│   │   └── Planilha original
│   └── processed/
│       └── Planilha processada
├── src/
│   └── pipeline.py
└── README.md
```

## Pipeline de dados

O arquivo `src/pipeline.py` reúne o código onde construí as camadas Bronze, Silver e Gold.

A planilha original está armazenada em `data/brutos/`, enquanto a planilha resultante do processamento está em `data/processed/`. Nesta última, encontram-se as abas correspondentes às camadas Bronze, Silver, Gold e Log.
