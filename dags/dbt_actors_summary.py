"""
Run a dbt Core project as a task group with Cosmos

Simple DAG showing how to run a dbt project as a task group, using
an Airflow connection and injecting a variable into the dbt project.
"""

from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig

from datetime import datetime, timedelta
import os

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

DBT_PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/dbt/clickhouse_demo"
DBT_EXECUTABLE_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"

profile_config = ProfileConfig(
    profile_name="clickhouse_imdb",
    target_name="dev",
    profiles_yml_filepath=f"{DBT_PROJECT_PATH}/profiles.yml"
)

execution_config = ExecutionConfig(
    dbt_executable_path=DBT_EXECUTABLE_PATH,
)


with DAG(
    "dbt_actors_summary",
    default_args=default_args,
    description=__doc__,
    schedule_interval=None, # timedelta(minutes=15),
    start_date=days_ago(1),
    catchup=False,
    tags=["dbt", "clickhouse", "actors"],
) as dag:
    @task
    def start_processing():
        return "Starting DBT processing"


    @task
    def end_processing(status):
        return f"Completed DBT processing: {status}"


    # Create the DbtTaskGroup outside of any task function
    transform_data = DbtTaskGroup(
        group_id="transform_data",
        project_config=ProjectConfig(DBT_PROJECT_PATH),
        profile_config=profile_config,
        execution_config=execution_config,
        default_args=default_args,
    )

    # Set up the task dependencies
    start = start_processing()
    end = end_processing("success")

    start >> transform_data >> end