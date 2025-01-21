## ------------ Imports ------------ ##
from pyspark.sql import SparkSession
import pyspark.sql.functions as F



## ------------ Defaults/Variables ------------ ##
# Create a SparkSession
spark = SparkSession.builder.appName("dim_customers").getOrCreate()



## ------------ Functions ------------ ##
def spark_read_json_as_df(filepath:str):
    """ Returns a Spark DataFrame with the given json file"""
    df = spark.read.json(filepath)
    return df


def select_transaction_cols(df):
    """ This function selects the transaction columns in the DataFrame"""
    df = df.select("transaction_id", "transaction_datetime")
    return df


## ------------ main ------------ ##
def main(filepath):
    df = spark_read_json_as_df(filepath)
    df = select_transaction_cols(df)
    df.write.parquet("etl/dim_transactions.parquet")
