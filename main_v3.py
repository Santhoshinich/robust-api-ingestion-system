import yaml
import logging
from src.ingestion.api_client_v3 import APIClient
from src.utils.storage import save_raw, save_processed
from src.utils.logger import setup_logger


def load_config():
    with open("src/config/config.yaml", "r") as f:
        return yaml.safe_load(f)


def main():
    setup_logger()
    logging.info("Starting ingestion pipeline")

    config = load_config()

    client = APIClient(config["base_url"])
    endpoint_name = "posts"
    endpoint = config["endpoints"][endpoint_name]
    page_size = config["pagination"]["page_size"]

    all_data = []

    for page in client.fetch_paginated_data(endpoint, page_size):
        logging.info(f"Fetched page with {len(page)} records")
        all_data.extend(page)

    save_raw(all_data, endpoint_name)
    save_processed(all_data, endpoint_name)

    logging.info(f"Total records processed: {len(all_data)}")


if __name__ == "__main__":
    main()