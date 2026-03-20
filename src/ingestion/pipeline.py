import logging
from src.utils.metadata import get_last_id, update_last_id
from src.utils.metadata import (
    get_last_id,
    update_last_id,
    get_last_timestamp,
    update_timestamp
)

class DataPipeline:
    def __init__(self, client, storage, transformer):
        self.client = client
        self.storage = storage
        self.transformer = transformer

    def run(self, endpoint_name, endpoint, page_size):
        logging.info(f"Running pipeline for {endpoint_name}")

        last_id = get_last_id(endpoint_name)
        last_ts = get_last_timestamp(endpoint_name)

        logging.info(f"Last ID: {last_id}, Last Timestamp: {last_ts}")

        all_data = []

        for page in self.client.fetch_paginated_data(endpoint, page_size):
            new_records = []

            for r in page:
                record_id = r.get("id", 0)
                record_ts = r.get("updated_at")

            # Dual logic
                if last_ts:
                    if record_ts and record_ts > last_ts:
                        new_records.append(r)
                else:
                    if record_id > last_id:
                        new_records.append(r)

            if new_records:
                all_data.extend(new_records)

        if not all_data:
            logging.info("No new data to process")
            return

    # Save raw
        self.storage.save_raw(all_data, endpoint_name)

    # Transform
        processed_data = self.transformer.transform(all_data)

    # Save processed
        self.storage.save_processed(processed_data, endpoint_name)

    # Update watermark
        max_id = max(r.get("id", 0) for r in all_data)
        update_last_id(endpoint_name, max_id)

    # Update timestamp (if available)
        timestamps = [r.get("updated_at") for r in all_data if r.get("updated_at")]
        if timestamps:
            latest_ts = max(timestamps)
            update_timestamp(endpoint_name, latest_ts)
            logging.info(f"Updated timestamp to {latest_ts}")

        logging.info(f"Updated last_id to {max_id}")