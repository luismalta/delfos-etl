# Delfos ETL

## Tecnologias
- Python
- Pandas
- Dagster
- SQLAlchemy
- PostgreSQL
- Docker

## Como Rodar

### Pré-requisitos
- Docker

### Passos para execução

1. Clone o repositório:
    ```bash
    git clone https://github.com/luismalta/delfos-etl.git
    cd delfos-etl
    ```

2. Copie os arquivos .env da API e do Dagster:
    ```bash
    cp source_db/example.env source_db/.env
    cp etl/example.env etl/.env
    ```
3. Build e suba o compose do projeto
    ```bash
    docker compose up --build
    ```
4. O Swagger da API estará disponível em http://localhost:8000/docs

5. O Dagster UI estára disponível em http://localhost:3000/
   
### O que o compose do projeto irá subir

O `docker compose` do projeto irá subir os seguintes serviços:
- **API**: Encapsulamento do banco de dados fonte utilizando o FastAPI.
- **Dagster**: Orquestrador de tarefas ETL.
- **PostgreSQL (Fonte)**: Banco de dados relacional utilizado como fonte de dados.
- **PostgreSQL (Alvo)**: Banco de dados relacional utilizado para armazenar os dados processados.
- **pgAdmin**: Ferramenta de administração para PostgreSQL.

Todo o setup e inicialização dos bancos de dados serão executados automaticamente, garantindo que o ambiente esteja pronto para uso sem a necessidade de configurações manuais adicionais.

### ETL
- A ETL no Dagster foi particionado diáriamente, tendo um agendador para executar o job de materialização dos assets todos os dias a meia noite.
- O intervalo de dados geras está entre os dias **13/11/2024 e 22/11/2024**. Esses dados podem ser analizados no arquivo `source_db/scripts/dados_10_dias.csv`.
- Para realizar o ETL de todas as partições disponíveis, recomenda-se realizar o backfill de todos os assets do grupo `signal`.
