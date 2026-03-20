import json
import os
import pandas as pd
from datetime import datetime


def save_raw(data, endpoint):
    os.makedirs("data/raw", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"data/raw/{endpoint}_{timestamp}.json"

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def save_processed(data, endpoint):
    os.makedirs("data/processed", exist_ok=True)

    df = pd.DataFrame(data)

    # safety dedup
    if "id" in df.columns:
        df = df.drop_duplicates(subset=["id"])

    file_path = f"data/processed/{endpoint}_clean.csv"
    df.to_csv(file_path, index=False)