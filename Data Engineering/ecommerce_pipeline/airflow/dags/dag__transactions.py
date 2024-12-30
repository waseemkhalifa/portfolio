from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

import python_files.transactions as transactions



default_args = {
    "owner": "waseem",
    "retries": 1,
    "retry_delay":timedelta(minutes=5)
}



def task_1():
    transactions.get_transactions_load_s3()


with DAG(
    default_args=default_args,
    dag_id="transactions",
    description="extracts transactions and loads to s3",
    start_date=datetime(2024,12,29),
    schedule_interval="@daily"
) as dag:

    task1 = PythonOperator(
        task_id="get_transactions_load_s3",
        python_callable=task_1
    )

    task1
