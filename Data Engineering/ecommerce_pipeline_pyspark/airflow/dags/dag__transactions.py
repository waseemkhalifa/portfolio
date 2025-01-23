## ------------ Imports ------------ ##
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.python import PythonOperator

import python_files.ecommerce_dataset_generator.src.fake__transactions as faker_transactions
import python_files.export_list_as_json as export_list_as_json

import python_files.transform_load.dim_products as dim_products
import python_files.transform_load.dim_transactions as dim_transactions
import python_files.transform_load.dim_transactions_lineitem as dim_transactions_lineitem
import python_files.transform_load.fct_transactions as fct_transactions

import python_files.transform_load.load_to_redshift as d2f

import python_files.export_to_s3 as export_to_s3
import python_files.delete_file as remove_file
import python_files.import_from_s3 as import_files_from_s3
import python_files.delete_s3_file as remove_s3_files
import python_files.delete_folder as remove_directory



## ------------ Defaults/Variables ------------ ##
default_args = {
    "owner": "waseem",
    "retries": 1,
    "retry_delay":timedelta(minutes=5)
}

TRANSACTION_MIN = 5
TRANSACTION_MAX = 10
LOCAL_FILE = "transactions.json"
NAME_FOR_S3_FILE = "transactions"
CURRENT_DATETIME = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
DIRECTORY = "downloads"


## ------------ Python Callables ------------ ##
def task__get_transactions():
    return faker_transactions.get_transactions(TRANSACTION_MIN, TRANSACTION_MAX)


def task__list_to_json_file(ti):
    export_list_as_json.list_to_json_file(
        lst=ti.xcom_pull(task_ids="get_transactions"),
        file_name=LOCAL_FILE)


def task__save_file_to_s3():
    export_to_s3.save_file_to_s3(local_file=LOCAL_FILE, 
                                 file_name=NAME_FOR_S3_FILE+CURRENT_DATETIME+".json")


def task__delete_file():
    remove_file.delete_file(file_name=LOCAL_FILE)


def task__import_from_s3():
    import_files_from_s3.download_s3_files()


def task__transform():
    dim_products.main(directory=DIRECTORY)
    dim_transactions.main(directory=DIRECTORY)
    dim_transactions_lineitem.main(directory=DIRECTORY)
    fct_transactions.main(directory=DIRECTORY)


def task__load_to_redshift():
    # dim_products
    d2f.dataframe_to_redshift(
        df_parquet_filename="etl/dim_products.parquet",
        redshift_target_db="pyspark",
        redshift_target_schema="dimension",
        redshift_target_table="dim__products")
    
    # dim_transactions
    d2f.dataframe_to_redshift(
        df_parquet_filename="etl/dim_transactions.parquet",
        redshift_target_db="pyspark",
        redshift_target_schema="dimension",
        redshift_target_table="dim__transactions")
    
    # dim_transactions_lineitem
    d2f.dataframe_to_redshift(
        df_parquet_filename="etl/dim_transactions_lineitem.parquet",
        redshift_target_db="pyspark",
        redshift_target_schema="dimension",
        redshift_target_table="dim__transactions_lineitem")
    
    # fct_transactions
    d2f.dataframe_to_redshift(
        df_parquet_filename="etl/fct_transactions.parquet",
        redshift_target_db="pyspark",
        redshift_target_schema="fact",
        redshift_target_table="fct__transactions")


def task__delete_s3_file():
    remove_s3_files.delete_s3_file(directory=DIRECTORY)


def task__delete_folder():
    remove_directory.delete_folder(directory=DIRECTORY)
    remove_directory.delete_folder(directory="etl")



## ------------ Dags & Tasks ------------ ##
with DAG(
    default_args=default_args,
    dag_id="ETL",
    description="This is a pipeline of trasactions into Redshift",
    start_date=datetime(2024,12,29),
    # schedule_interval="@daily",
    schedule_interval=None,
    catchup=False,
) as dag:

    get_transactions = PythonOperator(
        task_id="get_transactions",
        python_callable=task__get_transactions
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


    transform = PythonOperator(
        task_id="transform",
        python_callable=task__transform
    )


    load_to_redshift = PythonOperator(
        task_id="load_to_redshift",
        python_callable=task__load_to_redshift
    )


    delete_s3_file = PythonOperator(
        task_id="delete_s3_file",
        python_callable=task__delete_s3_file
    )


    delete_folder = PythonOperator(
        task_id="delete_folder",
        python_callable=task__delete_folder
    )


    get_transactions >> list_to_json_file
    list_to_json_file >> save_file_to_s3
    save_file_to_s3 >> delete_local_file
    delete_local_file >> import_from_s3
    import_from_s3 >> transform
    transform >> load_to_redshift
    load_to_redshift >> delete_s3_file
    delete_s3_file >> delete_folder
