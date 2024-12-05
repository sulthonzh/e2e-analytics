import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Create DataFrame
data = {
    "product_id": [1, 2],
    "name": ["Product A", "Product B"],
    "category": ["Electronics", "Home"],
    "price": [199.99, 89.99],
}
df = pd.DataFrame(data)

# Write to Parquet
table = pa.Table.from_pandas(df)
pq.write_table(table, "/home/jovyan/data/sample.parquet")
print("Parquet file created.")
