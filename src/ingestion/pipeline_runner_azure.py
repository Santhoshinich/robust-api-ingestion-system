import yaml
import logging
import os

from src.utils.logger import setup_logger
from src.ingestion.api_client_v3 import APIClient
from src.ingestion.pipeline import DataPipeline
from src.processors.transformer_v1 import DataTransformer
import src.utils.storage_azure as storage


def load_config():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(BASE_DIR, "../config/config.yaml")
    CONFIG_PATH = os.path.abspath(CONFIG_PATH)

    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Config not found at {CONFIG_PATH}")

    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def run_pipeline(mode: str, endpoint: str):
    setup_logger()
    logging.info(f"[AZURE] Running pipeline | mode={mode}, endpoint={endpoint}")

    config = load_config()
    transformer = DataTransformer()

    if mode == "rest":
        if endpoint not in config["endpoints"]:
            raise ValueError(f"Invalid endpoint: {endpoint}")

        client = APIClient(config["base_url"])
        pipeline = DataPipeline(client, storage, transformer)

        pipeline.run(
            endpoint,
            config["endpoints"][endpoint],
            config["pagination"]["page_size"]
        )

    elif mode == "soap":
        from src.ingestion.soap_client import SOAPClient

        wsdl_url = "http://www.dneonline.com/calculator.asmx?WSDL"
        client = SOAPClient(wsdl_url)

        pipeline = DataPipeline(client, storage, transformer)

        pipeline.run_soap(
            endpoint_name="calculator",
            method="Add",
            params={"intA": 10, "intB": 20}
        )

    else:
        raise ValueError("Invalid mode")

    logging.info("[AZURE] Pipeline execution completed")
