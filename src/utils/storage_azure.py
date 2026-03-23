import json
import os
import logging
import pandas as pd
from datetime import datetime
from azure.storage.blob import BlobServiceClient


AZURE_CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
RAW_CONTAINER = "raw"
PROCESSED_CONTAINER = "processed"


def _get_blob_client(container, blob_name):
    service = BlobServiceClient.from_connection_string(AZURE_CONN_STR)
    return service.get_blob_client(container=container, blob=blob_name)


def save_raw(data, endpoint):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    blob_name = f"{endpoint}/{endpoint}_{timestamp}.json"

    blob_client = _get_blob_client(RAW_CONTAINER, blob_name)
    blob_client.upload_blob(json.dumps(data, indent=2), overwrite=True)

    logging.info(f"Uploaded raw data to Azure Blob: {RAW_CONTAINER}/{blob_name}")


def save_processed(data, endpoint):
    df = pd.DataFrame(data)

    if "id" in df.columns:
        df = df.drop_duplicates(subset=["id"])

    blob_name = f"{endpoint}/{endpoint}_clean.csv"
    csv_data = df.to_csv(index=False)

    blob_client = _get_blob_client(PROCESSED_CONTAINER, blob_name)
    blob_client.upload_blob(csv_data, overwrite=True)

    logging.info(f"Uploaded processed data to Azure Blob: {PROCESSED_CONTAINER}/{blob_name}")
