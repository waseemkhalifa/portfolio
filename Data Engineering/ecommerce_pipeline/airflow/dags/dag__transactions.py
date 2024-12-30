## ------------ Imports ------------ ##
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

import python_files.faker_transactions as faker_transactions
import python_files.convert_dataclass_to_json as convert_dataclass_to_json
import python_files.export_list_as_json as export_list_as_json
import python_files.export_to_s3 as export_to_s3
import python_files.delete_file as remove_file



## ------------ Defaults/Variables ------------ ##
default_args = {
    "owner": "waseem",
    "retries": 1,
    "retry_delay":timedelta(minutes=5)
}

TRANSACTION_MIN = 1
TRANSACTION_MAX = 9
LOCAL_FILE = "transactions.json"
NAME_FOR_S3_FILE = 'transactions'
CURRENT_DATETIME = datetime.now().strftime("%Y-%m-%d %H-%M-%S")



## ------------ Python Callables ------------ ##
def task__get_transactions():
    transactions = faker_transactions.get_transactions(TRANSACTION_MIN, TRANSACTION_MAX)
    return transactions


def task__dataclass_to_json(ti):
    transactions = convert_dataclass_to_json.\
                    dataclass_to_json(dataclass_list=ti.xcom_pull(task_ids='get_transactions'))
    return transactions


def task__list_to_json_file(ti):
    export_list_as_json.list_to_json_file(lst=ti.xcom_pull(task_ids='dataclass_to_json'),
                                          file_name=LOCAL_FILE)


def task__save_json_file_to_s3(ti):
    export_to_s3.save_json_file_to_s3(local_file=LOCAL_FILE, 
                                      file_name=NAME_FOR_S3_FILE+CURRENT_DATETIME+".json")


def task__delete_file():
    remove_file.delete_file(file_name=LOCAL_FILE)



## ------------ Dags & Tasks ------------ ##
with DAG(
    default_args=default_args,
    dag_id="transactions",
    description="Pipeline",
    start_date=datetime(2024,12,29),
    schedule_interval="@daily"
) as dag:

    get_transactions = PythonOperator(
        task_id="get_transactions",
        python_callable=task__get_transactions
    )

    dataclass_to_json = PythonOperator(
        task_id="dataclass_to_json",
        python_callable=task__dataclass_to_json
    )

    list_to_json_file = PythonOperator(
        task_id="list_to_json_file",
        python_callable=task__list_to_json_file
    )

    save_json_file_to_s3 = PythonOperator(
        task_id="save_json_file_to_s3",
        python_callable=task__save_json_file_to_s3
    )

    delete_file = PythonOperator(
        task_id="delete_local_file",
        python_callable=task__delete_file
    )

    get_transactions>>dataclass_to_json
    dataclass_to_json>>list_to_json_file
    list_to_json_file>>save_json_file_to_s3
    save_json_file_to_s3>>delete_file
    