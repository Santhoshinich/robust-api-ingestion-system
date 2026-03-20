import json
import os

METADATA_PATH = "data/metadata.json"


def load_metadata():
    import json
    import os

    if not os.path.exists(METADATA_PATH):
        return {}

    try:
        with open(METADATA_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_metadata(metadata):
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=2)


def get_last_id(endpoint):
    metadata = load_metadata()
    return metadata.get(endpoint, {}).get("last_id", 0)


def update_last_id(endpoint, last_id):
    metadata = load_metadata()

    if endpoint not in metadata:
        metadata[endpoint] = {}

    metadata[endpoint]["last_id"] = last_id

    save_metadata(metadata)

def get_last_timestamp(endpoint):
    metadata = load_metadata()
    return metadata.get(endpoint, {}).get("last_updated_at")


def update_timestamp(endpoint, timestamp):
    metadata = load_metadata()

    if endpoint not in metadata:
        metadata[endpoint] = {}

    metadata[endpoint]["last_updated_at"] = timestamp

    save_metadata(metadata)