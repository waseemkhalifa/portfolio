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
import python_files.import_from_s3 as import_files_from_s3
import python_files.combine_json_list as combine_json_to_list
import python_files.df_to_redshift as dataframe_to_redshift
import python_files.delete_s3_file as remove_s3_files
import python_files.delete_folder as remove_directory



## ------------ Defaults/Variables ------------ ##
default_args = {
    "owner": "waseem",
    "retries": 1,
    "retry_delay":timedelta(minutes=5)
}

TRANSACTION_MIN = 1
TRANSACTION_MAX = 9
LOCAL_FILE = "transactions.json"
NAME_FOR_S3_FILE = "transactions"
CURRENT_DATETIME = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
DIRECTORY = "downloads"
TARGET_REDSHIFT_DB = "prod"
TARGET_REDSHIFT_SCHEMA = "datalake"
TARGET_REDSHIFT_TABLE = "faker__transactions"


## ------------ Python Callables ------------ ##
def task__get_transactions():
    return faker_transactions.get_transactions(TRANSACTION_MIN, TRANSACTION_MAX)


def task__dataclass_to_json(ti):
    return convert_dataclass_to_json\
        .dataclass_to_json(dataclass_list=ti.xcom_pull(task_ids="get_transactions"))


def task__list_to_json_file(ti):
    export_list_as_json.list_to_json_file(
        lst=ti.xcom_pull(task_ids="dataclass_to_json"),
        file_name=LOCAL_FILE)


def task__save_file_to_s3():
    export_to_s3.save_file_to_s3(local_file=LOCAL_FILE, 
                                 file_name=NAME_FOR_S3_FILE+CURRENT_DATETIME+".json")


def task__delete_file():
    remove_file.delete_file(file_name=LOCAL_FILE)


def task__import_from_s3():
    import_files_from_s3.download_s3_files()


def task__combine_json_list():
    return combine_json_to_list.json_files_list(directory=DIRECTORY)


def task__df_to_redshift(ti):
    dataframe_to_redshift.upload_df_to_redshift(
        transaction_json_list=ti.xcom_pull(task_ids="combine_json_list"),
        target_redshift_db=TARGET_REDSHIFT_DB,
        target_redshift_schema=TARGET_REDSHIFT_SCHEMA,
        target_redshift_table=TARGET_REDSHIFT_TABLE)


def task__delete_s3_file():
    remove_s3_files.delete_s3_file(directory=DIRECTORY)


def task__delete_folder():
    remove_directory.delete_folder(directory=DIRECTORY)



## ------------ Dags & Tasks ------------ ##
with DAG(
    default_args=default_args,
    dag_id="transactions",
    description="This is a pipeline of trasactions into Redshift",
    start_date=datetime(2024,12,29),
    schedule_interval="@daily",
    catchup=False,
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


    save_file_to_s3 = PythonOperator(
        task_id="save_file_to_s3",
        python_callable=task__save_file_to_s3
    )


    delete_local_file = PythonOperator(
        task_id="delete_local_file",
        python_callable=task__delete_file
    )


    import_from_s3 = PythonOperator(
        task_id="import_from_s3",
        python_callable=task__import_from_s3
    )


    combine_json_list = PythonOperator(
        task_id="combine_json_list",
        python_callable=task__combine_json_list
    )


    df_to_redshift = PythonOperator(
        task_id="df_to_redshift",
        python_callable=task__df_to_redshift
    )


    delete_s3_file = PythonOperator(
        task_id="delete_s3_file",
        python_callable=task__delete_s3_file
    )

    delete_folder = PythonOperator(
        task_id="delete_folder",
        python_callable=task__delete_folder
    )


    get_transactions >> dataclass_to_json
    dataclass_to_json >> list_to_json_file
    list_to_json_file >> save_file_to_s3
    save_file_to_s3 >> delete_local_file
    delete_local_file >> import_from_s3
    import_from_s3 >> combine_json_list
    combine_json_list >> df_to_redshift
    df_to_redshift >> delete_s3_file
    delete_s3_file >> delete_folder
