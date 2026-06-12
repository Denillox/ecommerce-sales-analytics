from azure.storage.blob import BlobServiceClient
import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

# Testing connection to Azure
storage_conn = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
sql_conn = os.getenv("AZURE_SQL_CONNECTION_STRING")

# Storage Account connection
try:
    blob_service = BlobServiceClient.from_connection_string(storage_conn)
    print("Storage Account connected successfully!")
except Exception as e:
    print(f"Storage connection failed: {e}")

# SQL Database connection
try:
    connection = pyodbc.connect(sql_conn)
    print("SQL Database connected successfully!")
except Exception as e:
    print(f"SQL connection failed: {e}")