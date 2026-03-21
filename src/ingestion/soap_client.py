from zeep import Client
import logging


class SOAPClient:
    def __init__(self, wsdl_url):
        self.client = Client(wsdl_url)

    def fetch_data(self, method, params=None):
        try:
            logging.info(f"Calling SOAP method: {method}")

            service = self.client.service

            if params:
                response = getattr(service, method)(**params)
            else:
                response = getattr(service, method)()

            return self._normalize_response(response)

        except Exception as e:
            logging.error(f"SOAP request failed: {e}")
            raise

    def _normalize_response(self, response):
        """
        Ensure response is always a list of dicts
        """

        # primitive types (int, float, str)
        if isinstance(response, (int, float, str)):
            return [{"result": response}]

        # dictionary
        if isinstance(response, dict):
            return [response]

        # list
        if isinstance(response, list):
            return response

        # fallback
        return [{"result": str(response)}]