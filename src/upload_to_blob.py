from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to blob storage
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get the container
container_name = "raw-data"
container_client = blob_service_client.get_container_client(container_name)


for file in os.listdir("data/raw"):
    with open(f"data/raw/{file}", "rb") as data:
        container_client.upload_blob(name=file, data=data)
        print(f"Uploaded {file} successfully")
