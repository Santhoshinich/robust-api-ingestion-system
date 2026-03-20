import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_data(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"API call failed: {response.status_code}")

        return response.json()