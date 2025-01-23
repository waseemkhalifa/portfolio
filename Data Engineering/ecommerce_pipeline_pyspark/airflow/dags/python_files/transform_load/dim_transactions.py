## ------------ Imports ------------ ##
import sys
sys.path.append("/home/waseem/Documents/Self-Development/git_repos/portfolio/Data Engineering/ecommerce_pipeline_pyspark/airflow/dags/python_files/transform_load")

from pyspark.sql import SparkSession
import pyspark.sql.functions as F

import json_to_spark_df as jsdf



## ------------ Defaults/Variables ------------ ##
# Create a SparkSession
spark = SparkSession.builder.appName("dim_transactions").getOrCreate()



## ------------ Functions ------------ ##
def select_transaction_cols(df):
    """ This function selects the transaction columns in the DataFrame"""
    df = df.select("transaction_id", "transaction_datetime")
    return df


## ------------ main ------------ ##
def main(directory):
    df = jsdf.spark_read_json_as_df(directory)
    df = select_transaction_cols(df)
    df.write.parquet("etl/dim_transactions.parquet")
