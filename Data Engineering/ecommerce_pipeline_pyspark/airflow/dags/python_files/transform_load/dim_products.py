## ------------ Imports ------------ ##
from pyspark.sql import SparkSession
import pyspark.sql.functions as F



## ------------ Defaults/Variables ------------ ##
# Create a SparkSession
spark = SparkSession.builder.appName("dim_products").getOrCreate()



## ------------ Functions ------------ ##
def spark_read_json_as_df(filepath:str):
    """ Returns a Spark DataFrame with the given json file"""
    df = spark.read.json(filepath)
    return df


def unnest_product_col(df):
    """ This function unnests the product array column in the DataFrame"""
    df = df.select("transaction_id", "product",
                   F.col("product.product_id").alias("product_id"),
                   F.col("product.product_category").alias("product_category"),
                   F.col("product.product_price").alias("product_price"))
    return df


def explode_product_cols(df):
    """ This function explodes the Product array columns"""
    df = df.withColumn("new", F.arrays_zip("product_id",
                                           "product_category",
                                           "product_price"))\
            .withColumn("new", F.explode("new"))\
            .select("transaction_id", 
                    F.col("new.product_id").alias("product_id"), 
                    F.col("new.product_category").alias("product_category"), 
                    F.col("new.product_price").alias("product_price"))
    return df



## ------------ main ------------ ##
def main(filepath):
    df = spark_read_json_as_df(filepath)
    df = unnest_product_col(df)
    df = explode_product_cols(df)
    df.write.parquet("etl/dim_products.parquet")
