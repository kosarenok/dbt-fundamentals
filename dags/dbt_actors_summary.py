"""
Run a dbt Core project as a task group with Cosmos
"""

from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig

from datetime import timedelta
from config.variables import DBT_EXECUTABLE_PATH, DBT_PROJECT_PATH

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

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
        """Execute before the DBT task group"""
        return "Starting DBT processing"


    @task
    def end_processing(status):
        """Execute after the DBT task group"""
        return f"Completed DBT processing: {status}"

    # Define a dbt task group for the actors_summary model
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