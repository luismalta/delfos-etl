FROM  python:3.12-slim

RUN pip install SQLAlchemy==2.0.36 psycopg2-binary

COPY create_tables.py create_tables.py

ENTRYPOINT ["python", "create_tables.py" ]

