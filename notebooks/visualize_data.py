import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import trino

# Configure logger
logging.basicConfig(filename='/home/jovyan/notebooks/data_visualization.log', 
                    level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

# Establish a connection to TrinoDB
conn = trino.dbapi.connect(
    host='trino',
    port=8080,
    user='admin',
    catalog='minio',
    schema='data_ingestion'
)

# Query data
try:
    cursor = conn.cursor()
    query = """
        SELECT s.sales_id, s.date, s.amount, p.name, p.category
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
    """
    cursor.execute(query)
    data = cursor.fetchall()
    columns = ["sales_id", "date", "amount", "name", "category"]
    sales_df = pd.DataFrame(data, columns=columns)
    logging.info("Data queried successfully for visualization.")

    # Visualize total sales per category
    total_sales_per_category = sales_df.groupby("category")["amount"].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x="category", y="amount", data=total_sales_per_category)
    plt.title("Total Sales per Product Category")
    plt.xlabel("Product Category")
    plt.ylabel("Total Sales ($)")
    plt.xticks(rotation=45)
    plt.savefig('/home/jovyan/notebooks/sales_per_category.png')
    logging.info("Visualization saved as 'sales_per_category.png'.")
except Exception as e:
    logging.error(f"Error visualizing data: {e}")
