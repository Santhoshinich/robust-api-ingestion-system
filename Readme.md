# 🚀 API Ingestion Engine

## 📌 Overview

This project implements a **production-grade data ingestion pipeline** supporting both **REST and SOAP APIs**, with **incremental processing, data quality validation, Airflow orchestration, and real-time alerting**.

It simulates a **real-world data engineering system** with modular design, observability, and workflow automation.

---

## ⚙️ Features

### 🔌 Ingestion

* REST API ingestion (JSON, pagination, retry)
* SOAP API integration (WSDL, XML → structured data)
* Unified processing framework for REST + SOAP

### 🔁 Incremental Processing

* ID-based watermarking
* Timestamp-based ingestion
* Idempotent pipeline execution
* CDC simulation (Insert/Update/Delete)

### 📊 Data Quality Layer (NEW 🚀)

* Required field validation
* Null checks
* Endpoint-specific rules
* Fail-fast validation (breaks pipeline on bad data)

### ⚡ Orchestration (Airflow - NEW 🚀)

* Dockerized Apache Airflow
* Dynamic DAG generation (config-driven)
* Parallel REST ingestion tasks
* Dependency chaining (REST → SOAP)

### 📡 Observability & Alerting (NEW 🚀)

* Structured logging across pipeline
* Airflow UI monitoring
* Slack alerts on task failure (real-time) — includes DAG, task, time, error, and clickable log link

### ☁️ Azure-Native Migration (NEW 🚀)

* **Azure Blob Storage** — Raw JSON + processed CSV in `raw/` and `processed/` containers
* **Azure Data Factory (ADF)** — Pipeline orchestration with Copy Activity + Mapping Data Flows + daily schedule trigger
* **Azure Key Vault** — Secure secrets management (Slack webhook, storage connection string)
* **Azure Container Registry (ACR)** — Dockerized pipeline image
* **Mapping Data Flows** — JSON flattening, column selection, deduplication for posts/comments/users
* SOAP XML response parsed to clean numeric result and stored as CSV

### 🧩 Architecture Design

* Config-driven pipelines (`config.yaml`)
* Modular components:

  * API clients
  * Pipeline engine
  * Transformer
  * Storage layer
  * Metadata tracking

---

## 🏗️ Architecture

### Local (Airflow + Docker)

```plaintext
REST APIs ───────┐
                 │
                 ▼
           API Client
                 │
                 ▼
             Pipeline
                 │
     ┌───────────┼───────────┐
     ▼           ▼           ▼
Transformer   Data Quality   Metadata
     │           │           │
     └──────► Storage ◄──────┘
                 │
        Raw / Processed Data

SOAP API ──► SOAP Client ──► Same Pipeline
```

### Azure-Native (ADF + Blob Storage)

```plaintext
REST APIs ──► ADF Copy Activity ──► Azure Blob (raw/)
                                         │
                                         ▼
                                 Mapping Data Flow
                                 (flatten, select, dedup)
                                         │
                                         ▼
                                 Azure Blob (processed/)

SOAP API ──► ADF Web Activity ──► Parse XML ──► Azure Blob (raw/ + processed/)

Any Failure ──► Slack Alert (ADF Web Activity)
Daily Schedule ──► ADF Trigger ──► Full Pipeline
```

---

## 🔄 Workflow

### Airflow DAG (Local)

```plaintext
rest_posts ──┐
rest_users ──┼──► soap_calculator
rest_comments┘
```

* REST tasks run **in parallel**
* SOAP runs **after REST completion**
* Fully **dynamic DAG based on config**

### ADF Pipeline (Azure) — 9 Activities

```plaintext
IngestPosts ──► TransformPosts
IngestComments ──► TransformComments
IngestUsers ──► TransformUsers
IngestUsers ──► SOAPCalculator ──► SaveSOAPResult ──► TransformSOAP

Any failure ──► SlackAlertOnFailure
```

---

## 📂 Project Structure

```plaintext
api_ingestion_engine/
│
├── src/
│   ├── ingestion/
│   │   ├── api_client_v3.py          # REST client with pagination + retry
│   │   ├── soap_client.py            # SOAP client (zeep)
│   │   ├── pipeline.py               # Core pipeline logic
│   │   ├── pipeline_runner.py        # Local runner
│   │   └── pipeline_runner_azure.py  # Azure Blob runner
│   ├── processors/
│   │   └── transformer_v1.py         # Pandas transformer
│   └── utils/
│       ├── storage.py                # Local file storage
│       ├── storage_azure.py          # Azure Blob Storage
│       ├── metadata.py               # Watermark tracking
│       ├── data_quality.py           # Validation checks
│       ├── alerts.py                 # Slack alerts
│       ├── retry.py                  # Exponential backoff
│       └── logger.py                 # Structured logging
│
├── dags/
│   ├── api_ingestion_dynamic_dag.py  # Airflow DAG (local)
│   └── api_ingestion_azure_dag.py    # Airflow DAG (Azure storage)
│
├── airflow-docker/
│   ├── docker-compose.yaml           # Local Airflow setup
│   └── docker-compose-azure.yaml     # Azure-integrated Airflow setup
│
├── Dockerfile                        # Container image for pipeline
├── requirements.txt
├── main_v6.py
├── tests/
└── .github/workflows/pipeline.yml
```

---

## ▶️ How to Run

### 🔹 Local (CLI)

```bash
python main_v6.py --mode rest --endpoint posts
python main_v6.py --mode soap --endpoint calculator
```

### 🔹 Airflow (Docker)

```bash
cd airflow-docker
docker-compose up
```

Access UI: `http://localhost:8080`

### 🔹 Azure (ADF)

```bash
az datafactory pipeline create-run \
  --resource-group api-ingestion-rg \
  --factory-name apiingestionadf \
  --name api-ingestion-pipeline
```

---

## 🔄 Evolution of the Pipeline (v1 → v7)

### 🟢 v1 — Basic API Call

* Single script
* No structure

### 🟢 v2 — Pagination + Storage

* Pagination support
* Raw + processed storage

### 🟢 v3 — Retry + Logging

* Exponential backoff
* Structured logs

### 🟢 v4 — CLI + Config

* CLI arguments
* Config-driven design

### 🟢 v5 — Modular + Incremental

* Pipeline architecture
* Watermarking (ID + timestamp)

### 🟢 v6 — SOAP + CDC + CI/CD

* SOAP integration
* CDC simulation
* GitHub Actions

### 🔥 v7 — Production Orchestration

* Airflow DAG (dynamic)
* Parallel task execution
* Data quality validation layer
* Slack alert integration (DAG, task, time, error, log link)
* Dockerized orchestration

### 🔥 v8 — Azure-Native Migration (CURRENT)

* Azure Blob Storage (raw + processed layers)
* Azure Data Factory — 9-activity pipeline with daily trigger
* Azure Key Vault — secrets management
* Azure Container Registry — Docker image hosting
* Mapping Data Flows — JSON flattening, deduplication, CSV output
* SOAP XML parsing within ADF expressions
* Slack alerts from ADF on failure

---

## 📊 Outputs

| Layer | Local | Azure |
|---|---|---|
| Raw | `data/raw/*.json` | `Azure Blob: raw/` |
| Processed | `data/processed/*.csv` | `Azure Blob: processed/` |
| Metadata | `data/metadata.json` | ADF pipeline run history |
| Logs | Airflow UI + `logs/app.log` | ADF Monitor |

---

## 🚨 Alerting (NEW)

* Slack webhook integration
* Real-time alerts on:

  * Task failure
  * Data quality failure
* Includes DAG, task, and error details

---

## 🧪 CI/CD

GitHub Actions:

* Runs on push and PR
* Installs dependencies
* Executes tests
* Validates pipeline integrity

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.11 |
| Data | Pandas, Requests, Zeep |
| Orchestration | Apache Airflow, Azure Data Factory |
| Cloud | Azure Blob Storage, Azure Key Vault, Azure Container Registry |
| Containerization | Docker, docker-compose |
| CI/CD | GitHub Actions |
| Alerting | Slack Webhooks |
| Config | PyYAML |
| Testing | Pytest |

---

## 📚 Key Learnings

* Designing scalable REST + SOAP ingestion pipelines
* Implementing incremental + idempotent processing with watermarking
* Building dynamic Airflow DAGs from config
* Migrating a local pipeline to Azure-native stack (ADF + Blob + Key Vault)
* Using ADF Mapping Data Flows for JSON flattening and transformation
* Parsing SOAP XML responses within ADF expressions
* Production-grade observability and alerting across local and cloud environments

---


## 👨‍💻 Author

Santhoshini ch

Designed and implemented a cloud-based data engineering pipeline on Azure, focusing on production-grade architecture, orchestration, and data reliability.
