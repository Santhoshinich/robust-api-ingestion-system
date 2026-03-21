# 🚀 API Ingestion Engine (Project 2)

## 📌 Overview

This project implements a **production-grade data ingestion pipeline** supporting both **REST and SOAP APIs**, with incremental processing, modular architecture, and CI/CD automation.

---

## ⚙️ Features

* 🔌 REST API ingestion (JSON, pagination, retry)
* 🧾 SOAP API integration (WSDL, XML → structured data)
* 🔁 Retry logic with exponential backoff
* 📊 Logging and observability
* 🧩 Modular pipeline architecture
* 🧠 Incremental loading:

  * ID-based watermarking
  * Timestamp-based ingestion
* 🔄 CDC simulation (Insert/Update/Delete)
* 💻 CLI-based execution
* 🧪 Testing with pytest
* ⚡ CI/CD with GitHub Actions

---

## 🏗️ Architecture

```plaintext
          ┌──────────────┐
          │  REST API    │
          └──────┬───────┘
                 │
          ┌──────▼───────┐
          │ API Client   │
          └──────┬───────┘
                 │
          ┌──────▼───────┐
          │              │
          │  Pipeline    │
          │              │
          └──────┬───────┘
                 │
          ┌──────▼────────┐
          │ Transformer   │
          └──────┬────────┘
                 │
          ┌──────▼────────┐
          │ Storage       │
          └──────┬────────┘
                 │
          ┌──────▼────────┐
          │ Metadata      │
          │ (Watermark)   │
          └───────────────┘

          ┌──────────────┐
          │  SOAP API    │
          └──────┬───────┘
                 │
          ┌──────▼───────┐
          │ SOAP Client  │
          └──────────────┘
```

---

## 🔌 API Integration

### REST

* JSON-based APIs
* Pagination using `limit` and `skip`
* Dynamic endpoint handling

### SOAP

* WSDL-based service integration
* XML → Python normalization
* Unified processing with REST pipeline

---

## 📂 Project Structure

```plaintext
api_ingestion_engine/
│
├── src/
│   ├── ingestion/
│   │   ├── api_client.py
│   │   ├── soap_client.py
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
├── main_v6.py
├── requirements.txt
└── .github/workflows/pipeline.yml
```

---

## ▶️ How to Run

### REST Pipeline

```bash
python main_v6.py --mode rest --endpoint posts
```

### SOAP Pipeline

```bash
python main_v6.py --mode soap --endpoint calculator
```

---

## 🔄 Evolution of the Pipeline (v1 → v6)

### 🟢 v1 — Basic API Call

* Single script
* Fetch data from REST API
* No structure, no modularity

---

### 🟢 v2 — Pagination + Storage

* Added pagination handling
* Stored raw (JSON) and processed (CSV) data
* Introduced basic project structure

---

### 🟢 v3 — Retry + Logging

* Implemented retry logic (exponential backoff)
* Added structured logging
* Improved fault tolerance

---

### 🟢 v4 — CLI + Config-Driven

* Added CLI (`--endpoint`)
* Config-driven pipeline (`config.yaml`)
* Removed hardcoded values

---

### 🟢 v5 — Modular Pipeline + Incremental Loading

* Introduced pipeline architecture
* Separated ingestion, transformation, storage
* Implemented:

  * ID-based incremental loading
  * Timestamp-based ingestion
* Added metadata tracking

---

### 🟢 v6 — SOAP Integration + Advanced Features

* Added SOAP client (WSDL-based integration)
* Unified REST + SOAP pipeline
* Implemented:

  * CDC simulation (Insert/Update/Delete)
  * Data normalization layer
* Added CI/CD with GitHub Actions

---

### 🚀 Final Version (Current)

* Modular, scalable pipeline
* Supports REST & SOAP
* Incremental + idempotent processing
* CI/CD enabled
* Production-style architecture

---

## 🔄 Incremental Processing

* Tracks last processed data using metadata
* Supports:

  * `last_id`
  * `updated_at`
* Ensures idempotent pipeline execution

---

## 📊 Outputs

* Raw → `data/raw/`
* Processed → `data/processed/`
* Logs → `logs/`
* Metadata → `data/metadata.json`

---

## 🧪 CI/CD

GitHub Actions pipeline:

* Runs on push and PR
* Installs dependencies
* Executes pipeline
* Runs tests

---

## 🛠️ Tech Stack

* Python
* Pandas
* Requests
* Zeep (SOAP client)
* PyYAML
* Pytest
* GitHub Actions

---

## 📚 Key Learnings

* Designing **modular data pipelines**
* Handling **REST and SOAP integrations**
* Implementing **incremental data processing**
* Managing **data consistency and idempotency**
* Applying **CI/CD to data engineering workflows**

---

## 🚀 Next Steps

* Add orchestration (Airflow / Azure Data Factory)
* Integrate cloud storage (S3 / ADLS)
* Implement real-time streaming (Kafka/Event Hub)

---

## 👨‍💻 Author

Santhoshini ch

Built as part of a **multi-cloud data engineering portfolio** focused on real-world system design and production readiness.
