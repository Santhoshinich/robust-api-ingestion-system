import yaml
from src.ingestion.api_client_v2 import APIClient
from src.utils.storage import save_raw, save_processed


def load_config():
    with open("src/config/config.yaml", "r") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()

    client = APIClient(config["base_url"])
    endpoint_name = "posts"
    endpoint = config["endpoints"][endpoint_name]
    page_size = config["pagination"]["page_size"]

    all_data = []

    for page in client.fetch_paginated_data(endpoint, page_size):
        print(f"Fetched page with {len(page)} records")
        all_data.extend(page)

    # Save raw
    save_raw(all_data, endpoint_name)

    # Save processed
    save_processed(all_data, endpoint_name)

    print(f"Total records processed: {len(all_data)}")


if __name__ == "__main__":
    main()