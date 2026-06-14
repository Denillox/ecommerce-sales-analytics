from azure.storage.blob import BlobServiceClient
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine
import urllib
from dotenv import load_dotenv
import os
import pyodbc

load_dotenv()

# Connect to Blob Storage
storage_conn = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(storage_conn)
container_client = blob_service_client.get_container_client("raw-data")

# Connect to Azure SQL
sql_conn_str = os.getenv("AZURE_SQL_CONNECTION_STRING")
params = urllib.parse.quote_plus(sql_conn_str)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
conn = pyodbc.connect(sql_conn_str)
cursor = conn.cursor()

# Adding data to the dim_customer table, loaded from the customers csv
blob_client = container_client.get_blob_client("customers.csv")
blob_data = blob_client.download_blob().content_as_text()
df = pd.read_csv(StringIO(blob_data))

# print(df.head())

# Truncate all tables before reloading instead of upsert since data is generated and changes every run
cursor.execute("DELETE FROM fact_ordereditem")
cursor.execute("DELETE FROM dim_customer")
cursor.execute("DELETE FROM dim_orders")
cursor.execute("DELETE FROM dim_product")
cursor.execute("DELETE FROM dim_date")
conn.commit()

df.to_sql('dim_customer', con=engine, if_exists='append', index=False)
print("dim_customer loaded successfully!")


# Adding data to the dim_products table, loaded from products.csv
blob_client = container_client.get_blob_client("products.csv")
blob_data = blob_client.download_blob().content_as_text()
df = pd.read_csv(StringIO(blob_data))
df.to_sql('dim_product', con=engine, if_exists='append', index=False)
print("dim_product loaded successfully!")


blob_client = container_client.get_blob_client("orders.csv")
blob_data = blob_client.download_blob().content_as_text()
df = pd.read_csv(StringIO(blob_data))
df = df.drop(columns=['customer_id']) # Drop customer_id from orders, it was only used to initially build the fact table
df.to_sql('dim_orders', con=engine, if_exists='append', index=False)
print("dim_orders loaded successfully!")


blob_client = container_client.get_blob_client("dim_date.csv")
blob_data = blob_client.download_blob().content_as_text()
df = pd.read_csv(StringIO(blob_data))
df.to_sql('dim_date', con=engine, if_exists='append', index=False)
print("dim_date loaded successfully!")


blob_client = container_client.get_blob_client("fact_ordereditem.csv")
blob_data = blob_client.download_blob().content_as_text()
df = pd.read_csv(StringIO(blob_data))
df.to_sql('fact_ordereditem', con=engine, if_exists='append', index=False)
print("fact_ordereditem loaded successfully!")
