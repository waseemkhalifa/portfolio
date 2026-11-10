from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import *


# ==================================================
# Create Spark Session
# ==================================================

spark = (
    SparkSession.builder
    .appName("customer-bronze-layer")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.6"
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# ==================================================
# Customer Event Schema
# ==================================================

customer_schema = StructType([
    StructField("event_id", StringType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("event_type", StringType(), True),
    StructField("event_timestamp", StringType(), True),
    StructField("channel", StringType(), True),
    StructField("contract_length_months", IntegerType(), True),
    StructField("renewal_discount", FloatType(), True)
])


# ==================================================
# Customer Stream
# ==================================================

customer_kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "customer-events")
    .load()
)

customer_parsed_df = (
    customer_kafka_df
    .select(col("value").cast("string"))
    .select(
        from_json(
            col("value"),
            customer_schema
        ).alias("data")
    )
    .select("data.*")
)

customer_query = (
    customer_parsed_df
    .writeStream
    .format("parquet")
    .option(
        "path",
        "./data/bronze/customer_events"
    )
    .option(
        "checkpointLocation",
        "./checkpoints/customer_events"
    )
    .outputMode("append")
    .start()
)


# ==================================================
# Keep Streams Running
# ==================================================

spark.streams.awaitAnyTermination()
