## ------------ Imports ------------ ##
from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.bash import BashOperator


## ------------ Defaults/Variables ------------ ##
default_args = {
    "owner": "waseem",
    "retries": 1,
    "retry_delay":timedelta(minutes=5)
}

PATH_DBT_PROJECT = '"/home/waseem/Documents/Self-Development/git_repos/portfolio/Data Engineering/ecommerce_pipeline/airflow/dags/dbt/dbt_faker_transactions"'
PATH_DBT_VENV = '"/home/waseem/Documents/Self-Development/git_repos/portfolio/Data Engineering/ecommerce_pipeline/dbt-env/bin/activate"'
PATH_AIRFLOW_HOME = '"/home/waseem/Documents/Self-Development/git_repos/portfolio/Data Engineering/ecommerce_pipeline/airflow"'

DBT_COMMAND_PREFIX = f"cd {PATH_AIRFLOW_HOME} && source {PATH_DBT_VENV} && cd {PATH_DBT_PROJECT} &&"


## ------------ Dags & Tasks ------------ ##
with DAG(
    default_args=default_args,
    dag_id="transform_dbt",
    description="Transform data in our Redshift DataLake",
    start_date=datetime(2025,1,1),
    # schedule_interval="@daily",
    schedule_interval=None,
    catchup=False,
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"{DBT_COMMAND_PREFIX} dbt run"
    )

    dbt_clean = BashOperator(
        task_id="dbt_clean",
        bash_command=f"{DBT_COMMAND_PREFIX} dbt clean"
    )

    dbt_run >> dbt_clean
