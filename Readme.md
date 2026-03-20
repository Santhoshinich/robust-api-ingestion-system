# 🚀 API Ingestion Engine (Project 2)

## 📌 Overview

This project implements a **production-style data ingestion pipeline** that retrieves data from external APIs, processes it, and stores it in structured formats.
It demonstrates core data engineering concepts such as **API integration, incremental loading, modular pipeline design, and CI/CD automation**.

---

## ⚙️ Features

* 🔌 REST API ingestion with pagination support
* 🔁 Retry logic with exponential backoff
* 📊 Structured logging for observability
* 🧩 Modular pipeline architecture (ingestion, transformation, storage)
* 🧠 Incremental loading:

  * ID-based watermarking
  * Timestamp-based ingestion (`updated_at`)
* 🔄 CDC simulation (Insert/Update/Delete handling)
* 🧪 Basic testing using `pytest`
* ⚡ CI/CD pipeline using GitHub Actions
* 💻 CLI-based execution

---

## 🏗️ Architecture

```
API Client → Data Pipeline → Transformer → Storage
                        ↓
                    Metadata (watermark)
```

### Components:

* **API Client** → Handles API calls, pagination, retry
* **Pipeline** → Orchestrates ingestion and processing
* **Transformer** → Cleans, deduplicates, and enriches data
* **Storage** → Saves raw and processed datasets
* **Metadata** → Tracks incremental progress

---

## 📂 Project Structure

```
api_ingestion_engine/
│
├── src/
│   ├── ingestion/
│   │   ├── api_client.py
│   │   └── pipeline.py
│   ├── processors/
│   │   └── transformer.py
│   ├── utils/
│   │   ├── logger.py
│   │   ├── retry.py
│   │   ├── storage.py
│   │   └── metadata.py
│   └── config/
│       └── config.yaml
│
├── tests/
│   └── test_pipeline.py
│
├── main_v5.py
├── requirements.txt
├── README.md
└── .github/workflows/pipeline.yml
```

---

## ▶️ How to Run

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Run pipeline

```
python main_v5.py --endpoint posts
```

### 3. Run tests

```
pytest
```

---

## 🔄 Incremental Loading Strategy

* Uses **watermarking** to track last processed data
* Supports:

  * `last_id` (basic incremental)
  * `updated_at` (advanced incremental)
* Prevents duplicate processing and ensures idempotency

---

## 📊 Example Output

* Raw data → `data/raw/` (JSON format)
* Processed data → `data/processed/` (CSV format)
* Logs → `logs/app.log`
* Metadata → `data/metadata.json`

---

## 🧪 CI/CD

GitHub Actions pipeline:

* Runs on every push / PR
* Installs dependencies
* Executes pipeline
* Runs tests

---

## 🛠️ Tech Stack

* Python
* Pandas
* Requests
* PyYAML
* Pytest
* GitHub Actions

---

## 📚 Key Learnings

* Designing **idempotent data pipelines**
* Implementing **incremental ingestion (ID + timestamp)**
* Handling unreliable APIs with **retry strategies**
* Building **modular and scalable data systems**
* Applying **CI/CD to data engineering workflows**

---

## 🚀 Next Steps

* Add orchestration (Airflow / Azure Data Factory)
* Integrate with cloud storage (AWS S3 / Azure Data Lake)
* Implement real-time streaming (Kafka / Event Hub)

---

## 👨‍💻 Author

Santhoshini ch

Built as part of a **multi-cloud data engineering portfolio** focused on real-world system design and production readiness.
