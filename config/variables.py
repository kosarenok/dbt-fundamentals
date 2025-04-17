import os

DBT_PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/dbt/clickhouse_demo"
DBT_EXECUTABLE_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"