from datetime import datetime, timedelta
import pandas as pd


class DataTransformer:
    def transform(self, data):
        df = pd.DataFrame(data)

        # handle both REST + SOAP
        if "id" in df.columns:
            base_time = datetime(2026, 1, 1)
            df["updated_at"] = df["id"].apply(
                lambda x: (base_time + timedelta(seconds=int(x))).isoformat()
            )

        # handle SOAP result case
        if "result" in df.columns:
            df["updated_at"] = datetime.utcnow().isoformat()

        columns = [col for col in df.columns if col in ["id", "userId", "title", "result", "updated_at"]]
        df = df[columns]

        if "id" in df.columns:
            df = df.drop_duplicates(subset=["id"])

        return df.to_dict(orient="records")