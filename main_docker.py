import argparse
import logging

from src.utils.logger import setup_logger
from src.ingestion.pipeline_runner import run_pipeline  # NEW


def main():
    setup_logger()
    logging.info("Starting pipeline system")

    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--mode", choices=["rest", "soap"], required=True)
    args = parser.parse_args()

    # 👇 THIS is where it goes
    run_pipeline(args.mode, args.endpoint)


if __name__ == "__main__":
    main()