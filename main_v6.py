import yaml
import logging
import argparse

from src.utils.logger import setup_logger
from src.ingestion.api_client_v3 import APIClient
from src.ingestion.pipeline import DataPipeline
from src.processors.transformer_v1 import DataTransformer
import src.utils.storage as storage


def load_config():
    with open("src/config/config.yaml", "r") as f:
        return yaml.safe_load(f)


def main():
    setup_logger()
    logging.info("Starting pipeline system")

    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--mode", choices=["rest", "soap"], required=True)
    args = parser.parse_args()

    config = load_config()

    endpoint_name = args.endpoint
    transformer = DataTransformer()

    if args.mode == "rest":
        if endpoint_name not in config["endpoints"]:
            raise ValueError(f"Invalid endpoint: {endpoint_name}")

        client = APIClient(config["base_url"])
        pipeline = DataPipeline(client, storage, transformer)

        pipeline.run(
            endpoint_name,
            config["endpoints"][endpoint_name],
            config["pagination"]["page_size"]
        )

    elif args.mode == "soap":
        from src.ingestion.soap_client import SOAPClient

        wsdl_url = "http://www.dneonline.com/calculator.asmx?WSDL"
        client = SOAPClient(wsdl_url)

        pipeline = DataPipeline(client, storage, transformer)

        # Example SOAP operation
        pipeline.run_soap(
            endpoint_name="calculator",
            method="Add",
            params={"intA": 10, "intB": 20}
        )


if __name__ == "__main__":
    main()