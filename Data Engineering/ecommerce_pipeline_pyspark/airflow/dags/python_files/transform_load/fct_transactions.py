## ------------ Imports ------------ ##
from pyspark.sql import SparkSession
import pyspark.sql.functions as F



## ------------ Defaults/Variables ------------ ##
# Create a SparkSession
spark = SparkSession.builder.appName("fct_transactions").getOrCreate()



## ------------ Functions ------------ ##
def spark_read_json_as_df(filepath:str):
    """ Returns a Spark DataFrame with the given json file"""
    df = spark.read.json(filepath)
    return df


def unnest_col(df):
    """ This function unnests the array columns in the DataFrame"""
    df = df.select("transaction_id", 
                   "transaction_datetime",
                   F.col("customer.customer_id").alias("customer_id"),
                   F.col("product.product_price").alias("product_price"))
    return df


def explode_product_cols(df):
    """ This function explodes the Product array columns"""
    df = df.withColumn("new", F.arrays_zip("product_price"))\
            .withColumn("new", F.explode("new"))\
            .select("transaction_id", 
                    "customer_id",
                    F.col("new.product_price").alias("product_price"))
    return df



## ------------ main ------------ ##
def main(filepath):
    df = spark_read_json_as_df(filepath)
    df = unnest_col(df)
    df = explode_product_cols(df)
    df = df.withColumn("product_price", df.product_price.cast("float"))
    df = df.groupBy("transaction_id", "customer_id").sum("product_price")
    df.write.parquet("etl/fct_transactions.parquet")
