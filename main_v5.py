import yaml
import logging
import argparse

from src.utils.logger import setup_logger
from src.ingestion.api_client_v3 import APIClient
from src.ingestion.pipeline import DataPipeline
from src.processors.transformer import DataTransformer
import src.utils.storage as storage


def load_config():
    with open("src/config/config.yaml", "r") as f:
        return yaml.safe_load(f)


def main():
    setup_logger()
    logging.info("Starting pipeline system")

    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True)
    args = parser.parse_args()

    config = load_config()

    endpoint_name = args.endpoint

    if endpoint_name not in config["endpoints"]:
        raise ValueError(f"Invalid endpoint: {endpoint_name}")

    client = APIClient(config["base_url"])
    transformer = DataTransformer()

    pipeline = DataPipeline(client, storage, transformer)

    pipeline.run(
        endpoint_name,
        config["endpoints"][endpoint_name],
        config["pagination"]["page_size"]
    )


if __name__ == "__main__":
    main()