from datetime import datetime, timedelta
import pandas as pd

class DataTransformer:
    def transform(self, data):
        df = pd.DataFrame(data)

        # simulate stable updated_at using id
        base_time = datetime(2026, 1, 1)

        if "id" in df.columns:
            df["updated_at"] = df["id"].apply(
                lambda x: (base_time + timedelta(seconds=int(x))).isoformat()
            )

        columns = [col for col in ["id", "userId", "title", "updated_at"] if col in df.columns]
        df = df[columns]

        df = df.drop_duplicates(subset=["id"])

        return df.to_dict(orient="records")