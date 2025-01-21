## ------------ Imports ------------ ##
from pyspark.sql import SparkSession
import pyspark.sql.functions as F



## ------------ Defaults/Variables ------------ ##
# Create a SparkSession
spark = SparkSession.builder.appName("dim_transactions_lineitem").getOrCreate()



## ------------ Functions ------------ ##
def spark_read_json_as_df(filepath:str):
    """ Returns a Spark DataFrame with the given json file"""
    df = spark.read.json(filepath)
    return df


def unnest_customer_col(df):
    """ This function unnests the customer array column in the DataFrame"""
    df = df.select(F.col("customer.customer_id").alias("customer_id"),
                   F.col("customer.customer_prefix").alias("customer_prefix"),
                   F.col("customer.first_name").alias("first_name"),
                   F.col("customer.last_name").alias("last_name"),
                   F.col("customer.customer_email").alias("customer_email"))
    return df


## ------------ main ------------ ##
def main(filepath):
    df = spark_read_json_as_df(filepath)
    df = unnest_customer_col(df)
    df.write.parquet("etl/dim_transactions_lineitem.parquet")
