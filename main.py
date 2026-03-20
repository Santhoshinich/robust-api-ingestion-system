import yaml
from src.ingestion.api_client import APIClient


def load_config():
    with open("src/config/config.yaml", "r") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()

    client = APIClient(config["base_url"])

    endpoint = config["endpoints"]["posts"]
    data = client.fetch_data(endpoint)

    print(f"Fetched {len(data)} records")


if __name__ == "__main__":
    main()