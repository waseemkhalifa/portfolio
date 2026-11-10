from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import *


# ==================================================
# Create Spark Session
# ==================================================

spark = (
    SparkSession.builder
    .appName("network-bronze-layer")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.6"
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# ==================================================
# Build Network Event Schema
# ==================================================

network_schema = StructType([
    # Common event fields
    StructField("event_id", StringType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("event_type", StringType(), True),
    StructField("region", StringType(), True),
    StructField("network_type", StringType(), True),
    StructField("event_timestamp", StringType(), True),

    # Call fields
    StructField("call_duration_seconds", IntegerType(), True),

    # Dropped call fields
    StructField("signal_strength", IntegerType(), True),

    # Data session fields
    StructField("data_used_mb", DoubleType(), True),
    StructField("session_duration_minutes", IntegerType(), True),

    # SMS fields
    StructField("message_count", IntegerType(), True),

    # Network outage fields
    StructField("affected_customers", IntegerType(), True),
    StructField("outage_duration_minutes", IntegerType(), True),

    # Roaming fields
    StructField("country", StringType(), True),

    # Speed test fields
    StructField("download_speed_mbps", DoubleType(), True),
    StructField("upload_speed_mbps", DoubleType(), True),
    StructField("latency_ms", IntegerType(), True)
])


# ==================================================
# Network Stream
# ==================================================

network_kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "network-events")
    .load()
)

network_parsed_df = (
    network_kafka_df
    .select(col("value").cast("string"))
    .select(
        from_json(
            col("value"),
            network_schema
        ).alias("data")
    )
    .select("data.*")
)

network_query = (
    network_parsed_df
    .writeStream
    .format("parquet")
    .option(
        "path",
        "./data/bronze/network_events"
    )
    .option(
        "checkpointLocation",
        "./checkpoints/network_events"
    )
    .outputMode("append")
    .start()
)


# ==================================================
# Keep Streams Running
# ==================================================

spark.streams.awaitAnyTermination()
