FROM  python:3.12-slim

RUN pip install poetry==1.8.4

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

WORKDIR /opt/dagster/app

COPY pyproject.toml poetry.lock workspace.yaml ./
COPY etl ./etl
RUN touch README.md

RUN poetry install && rm -rf $POETRY_CACHE_DIR

COPY dagster.yaml /opt/dagster/dagster_home/


EXPOSE 3000

ENTRYPOINT ["poetry", "run", "dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]