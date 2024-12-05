import logging
import trino
import pandas as pd

# Configure logger
logging.basicConfig(
    filename="/home/jovyan/notebooks/trino_queries.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
)

# Establish a connection to Trino
conn = trino.dbapi.connect(
    host="trino", port=8080, user="admin", catalog="minio", schema="data_ingestion"
)
cursor = conn.cursor()

# Create tables and add logging
try:
    # Create table for sample.json
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id INT,
            name VARCHAR,
            category VARCHAR,
            price DOUBLE
        ) WITH (
            external_location = 's3a://data-ingestion/sample.json',
            format = 'JSON'
        )
    """
    )
    logging.info("Table 'products' created successfully.")

    # Create table for sample.csv
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            sales_id INT,
            product_id INT,
            date DATE,
            amount DOUBLE
        ) WITH (
            external_location = 's3a://data-ingestion/sample.csv',
            format = 'CSV',
            skip_header_line_count = 1
        )
    """
    )
    logging.info("Table 'sales' created successfully.")

    # Create table for sample.parquet
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products_parquet (
            product_id INT,
            name VARCHAR,
            category VARCHAR,
            price DOUBLE
        ) WITH (
            external_location = 's3a://data-ingestion/sample.parquet',
            format = 'PARQUET'
        )
    """
    )
    logging.info("Table 'products_parquet' created successfully.")

except Exception as e:
    logging.error(f"Error creating tables: {e}")

# Query data
try:
    query = """
        SELECT s.sales_id, s.date, s.amount, p.name, p.category
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
    """
    cursor.execute(query)
    data = cursor.fetchall()
    columns = ["sales_id", "date", "amount", "name", "category"]
    sales_df = pd.DataFrame(data, columns=columns)
    logging.info("Data queried successfully.")

    # Output data
    print(sales_df)
except Exception as e:
    logging.error(f"Error querying data: {e}")
