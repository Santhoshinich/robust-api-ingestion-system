import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_paginated_data(self, endpoint, page_size=10):
        skip = 0

        while True:
            url = f"{self.base_url}{endpoint}?limit={page_size}&skip={skip}"
            response = requests.get(url)

            if response.status_code != 200:
                raise Exception(f"API call failed: {response.status_code}")

            data = response.json()
            posts = data.get("posts", [])

            if not posts:
                break

            yield posts

            skip += page_size

            if skip >= data.get("total", 0):
                break