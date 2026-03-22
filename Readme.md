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
* Slack alerts on task failure (real-time)

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

---

## 🔄 Airflow DAG Workflow (NEW)

```plaintext
rest_posts
rest_users
rest_comments
        ↓
   soap_calculator
```

* REST tasks run **in parallel**
* SOAP runs **after REST completion**
* Fully **dynamic DAG based on config**

---

## 📂 Project Structure

```plaintext
api_ingestion_engine/
│
├── src/
│   ├── ingestion/
│   ├── processors/
│   ├── utils/
│   └── config/
│
├── airflow-docker/
│   └── dags/
│
├── tests/
├── main_v6.py
├── requirements.txt
└── .github/workflows/
```

---

## ▶️ How to Run

### 🔹 Local (CLI)

```bash
python main_v6.py --mode rest --endpoint posts
python main_v6.py --mode soap --endpoint calculator
```

---

### 🔹 Airflow (Docker)

```bash
docker-compose up
```

Access UI:

```plaintext
http://localhost:8080
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

### 🔥 v7 — Production Orchestration (CURRENT)

* Airflow DAG (dynamic)
* Parallel task execution
* Data quality validation layer
* Slack alert integration
* Dockerized orchestration

---

## 📊 Outputs

* Raw → `data/raw/`
* Processed → `data/processed/`
* Metadata → `data/metadata.json`
* Logs → Airflow UI + local logs

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

* Python
* Pandas
* Requests
* Zeep (SOAP client)
* Apache Airflow (Docker)
* PyYAML
* Pytest
* GitHub Actions
* Slack Webhooks

---

## 📚 Key Learnings

* Designing scalable ingestion pipelines
* Handling REST + SOAP integration in one system
* Implementing incremental + idempotent processing
* Building dynamic Airflow DAGs
* Adding production-grade observability and alerting

---

## 🚀 Next Steps

* Migrate to Azure (ADLS Gen2)
* Integrate Azure Data Factory
* Implement cloud-native orchestration
* Add secrets management (Key Vault)

---

## 👨‍💻 Author

Santhoshini ch

Built as part of a **multi-cloud data engineering portfolio** focused on real-world system design and production readiness.
