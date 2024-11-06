import io
import os
import uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobBlock, BlobClient, StandardBlobTier

account_url = "https://tonipyrytimemanagement.blob.core.windows.net"
credential = DefaultAzureCredential()

def upload_blob_file(container_name: str, file_path: str, blob_name: str):
    # Create the BlobServiceClient object   
    blob_service_client = BlobServiceClient(account_url, credential=credential)
    # Get the container client
    container_client = blob_service_client.get_container_client(container_name)
    try:
        # Open the file in binary mode
        with open(file_path, mode="rb") as data:
            # Upload the file to the blob container
            container_client.upload_blob(blob_name, data, overwrite=True)
            print(f"File '{file_path}' uploaded as '{blob_name}' successfully!")
    
    except Exception as e:
        print(f"Error uploading file: {e}")

upload_blob_file("reports", "timelog_2024-11-05_15-18-04.txt", "timelog_2024-11-05_15-18-04")
