import requests
import logging
from src.utils.retry import retry


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    @retry(max_retries=3, backoff_factor=1)
    def make_request(self, url):
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code}")

        return response.json()

    def fetch_paginated_data(self, endpoint, page_size=10):
        skip = 0
        key = endpoint.strip("/")

        while True:
            url = f"{self.base_url}{endpoint}?limit={page_size}&skip={skip}"
            logging.info(f"Calling API: {url}")

            data = self.make_request(url)
            records = data.get(key, [])

            if not records:
                logging.info("No more data to fetch")
                break

            yield records

            skip += page_size

            if skip >= data.get("total", 0):
                break