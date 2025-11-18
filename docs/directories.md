# Estrutura dos diretórios
project/   
│   
├── data/   
│      ├── bronze/        # Dados brutos, “as is”   
│      ├── silver/        # Dados tratados e estruturados   
│      └── gold/          # Dados agregados e prontos para consumo   
│   
├── etl/   
│      ├── ingestion/     # Scripts para ingestão → bronze   
│      ├── transformation/   
│      │      ├── bronze_to_silver/   
│      │      └── silver_to_gold/   
│      ├── validation/    # Testes de qualidade (DQ)   
│      └── utils/         # Funções auxiliares   
│   
├── pipelines/   
│      ├── dags/          # Arquivos do Airflow / n8n / Prefect   
│      └── configs/       # Configurações das pipelines   
│   
├── docs/   
│      ├── data_dictionary/   
│      ├── architecture/   
│      └── readme.md   
│   
├── notebooks/         # Explorações, testes, protótipos   
│   
├── dashboards/   
│      ├── powerbi/   
│      ├── tableau/   
│      └── metabase/   
│   
├── tests/             # Testes automatizados (unitários e de integração)   
│   
├── configs/           # Configs globais (YAML/JSON/env)   
│   
└── requirements.txt   # Dependências   