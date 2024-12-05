import logging
from minio import Minio
import os

# Configure logger
logging.basicConfig(filename='/home/jovyan/notebooks/data_ingestion.log', 
                    level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

# Establish connection to MinIO
minio_client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Create bucket for data ingestion
bucket_name = "data-ingestion"
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)
    logging.info(f"Bucket '{bucket_name}' created.")

# Upload data files
data_files = ["sample.json", "sample.csv", "sample.parquet"]
for file_name in data_files:
    file_path = f"/home/jovyan/data/{file_name}"
    minio_client.fput_object(bucket_name, file_name, file_path)
    logging.info(f"{file_name} uploaded successfully to bucket '{bucket_name}'.")
