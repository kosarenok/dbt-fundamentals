# DBT Fundamentals Project

This project demonstrates the integration of **dbt (Data Build Tool)** with **Apache Airflow** and **ClickHouse** for
data transformation and orchestration. It uses **astronomer-cosmos** package to visualize dbt models inside Airflow UI. 
It includes a sample pipeline to process and summarize actor data from an IMDb-like dataset.

## Features

- **dbt** for data modeling and transformations.
- **Apache Airflow** for orchestration.
- **ClickHouse** as the database backend.
- Dockerized setup for easy deployment.

---

## Prerequisites

1. **Docker** and **Docker Compose** installed on your machine.
2. Python 3.11 installed (if running locally).
3. Environment variables configured in a `.env` file (see `.env.example` for reference).

---
## Screenshot of the Airflow UI with dbt models visualized:
<p>
  <img src="docs/images/example_dag.png" alt="DBT Pipeline in Airflow UI" width="3066"/>
  <br>
  <em>DBT models visualization in Airflow UI via astronomer-cosmos</em>
</p>

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/kosarenok/dbt-fundamentals.git
cd dbt-fundamentals
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```
AIRFLOW_DB_USER=airflow
AIRFLOW_DB_PASSWORD=airflow
AIRFLOW_DB_NAME=airflow
AIRFLOW_UID=50000
CLICKHOUSE_HOST=localhost # or ClickHouse container name
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=admin
```

### 3. Build and Start the Containers

```bash
docker-compose up -d
```

### 4. Access Airflow UI

Open your browser and navigate to `http://localhost:8080`. Log in with the credentials specified in the `.env` file.
The default username and password are both `admin`.

### 5. Run dbt locally

If you want to run dbt locally, make sure you have dbt environment set up.
```bash
export DBT_PROFILES_DIR=dags/dbt/clickhouse_demo
export DBT_PROJECT_DIR=dags/dbt/clickhouse_demo
```

