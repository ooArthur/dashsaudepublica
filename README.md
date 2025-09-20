# Dashboard Saúde - Vargem Grande

Este projeto é um **dashboard interativo em Streamlit** para análise de dados de saúde do município de Vargem Grande.  
Ele permite extrair, normalizar e visualizar tabelas do **SIOPS** (e futuramente de outras fontes como DataSUS), com exportação de dados normalizados.

---

## Estrutura do Projeto
```
datasaude_app/
│── Dashboard.py # Entrada principal do Streamlit (overview)
│── requirements.txt # Dependências Python
│── Dockerfile # Imagem Docker
│── docker-compose.yml # (opcional)
│
├── data/
│ ├── raw/ # CSVs extraídos
│ └── processed/ # CSVs normalizados
│
├── src/
│ ├── extract/ # Scripts de extração
│ ├── transform/ # Limpeza e normalização
│ └── dashboard/ # graficos dos dashs
│
└── pages/ # Páginas Streamlit (multipages)
```

---

## Funcionalidades Atuais

- Extração de dados do **SIOPS** por ano, bimestre e município.
- Visualização dos CSVs **brutos (RAW)** e **normalizados (PROCESSED)** diretamente na página de extração.
- Normalização de tabelas, tratamento de colunas duplicadas e limpeza de dados.
- Exclusão de arquivos **RAW** ou **PROCESSED** via botão no dashboard.
- Multipages no Streamlit, permitindo futuras adições de outras fontes de dados.

---

## Rodando o Projeto com Docker

1. **Build da imagem:**
```docker build -t dashboard-saude .```

2. **Rodar o container:**
```docker run -p 80801:8080 -v $(pwd)/data:/appdatasaude/data dashboard-saude```

> O volume `-v $(pwd)/data:/appdatasaude/data` mantém os arquivos RAW e PROCESSED persistentes fora do container.

3. **Acesse no navegador:**  
``http://localhost:8080``

---

## Dependências

As dependências estão listadas no `requirements.txt`:

- streamlit
- pandas
- requests
- beautifulsoup4

> Para rodar localmente sem Docker:  
> ```bash
> pip install -r requirements.txt
> streamlit run app.py
> ```

---

## Próximos Passos

- Adicionar outras fontes de dados (ex: DataSUS).
- Criar dashboards interativos por tabela ou indicadores agregados.
- Implementar gráficos interativos com **Altair** ou **Plotly**.
- Automatizar atualização de dados históricos.
