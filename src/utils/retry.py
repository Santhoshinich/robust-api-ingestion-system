import time
import logging


def retry(max_retries=3, backoff_factor=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0

            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    wait_time = backoff_factor * (2 ** retries)
                    logging.warning(
                        f"Retry {retries + 1}/{max_retries} after error: {e}. Waiting {wait_time}s"
                    )
                    time.sleep(wait_time)
                    retries += 1

            raise Exception(f"Failed after {max_retries} retries")

        return wrapper
    return decorator