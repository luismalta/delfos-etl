#!/bin/bash

# Variables
DATABASE="source_db"
TABLE="data"
CSV_FILE="/dados_10_dias.csv"
DB_USER="postgres"

# Check if the CSV file exists
if [ ! -f "$CSV_FILE" ]; then
    echo "CSV file '$CSV_FILE' not found!"
    exit 1
fi

# Populate the table
psql -U "$DB_USER" -d "$DATABASE" -c "\COPY $TABLE FROM '$CSV_FILE' DELIMITER ',' CSV HEADER;"

if [ $? -eq 0 ]; then
    echo "Table '$TABLE' in database '$DATABASE' populated successfully."
else
    echo "Failed to populate table '$TABLE' in database '$DATABASE'."
fi