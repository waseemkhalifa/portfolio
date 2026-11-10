from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import *


# ==================================================
# Create Spark Session
# ==================================================

spark = (
    SparkSession.builder
    .appName("billing-bronze-layer")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.6"
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# ==================================================
# Build Billing Event Schema
# ==================================================

billing_schema = StructType([
    # Common event fields
    StructField("event_id", StringType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("billing_account_id", IntegerType(), True),
    StructField("event_type", StringType(), True),
    StructField("event_timestamp", StringType(), True),
    StructField("currency", StringType(), True),

    # Billing fields
    StructField("bill_id", StringType(), True),
    StructField("bill_amount", DoubleType(), True),
    StructField("bill_period", StringType(), True),
    StructField("due_date", StringType(), True),

    # Payment fields
    StructField("payment_amount", DoubleType(), True),
    StructField("payment_method", StringType(), True),

    # Payment failure fields
    StructField("attempted_amount", DoubleType(), True),
    StructField("failure_reason", StringType(), True),

    # Direct debit fields
    StructField("bank_name", StringType(), True),
    StructField("mandate_id", StringType(), True),

    # Direct debit cancellation fields
    StructField("cancellation_reason", StringType(), True),

    # Refund fields
    StructField("refund_amount", DoubleType(), True),
    StructField("refund_reason", StringType(), True),

    # Late payment fields
    StructField("days_overdue", IntegerType(), True),
    StructField("outstanding_balance", DoubleType(), True)
])


# ==================================================
# Billing Stream
# ==================================================

billing_kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "billing-events")
    .load()
)

billing_parsed_df = (
    billing_kafka_df
    .select(col("value").cast("string"))
    .select(
        from_json(
            col("value"),
            billing_schema
        ).alias("data")
    )
    .select("data.*")
)

billing_query = (
    billing_parsed_df
    .writeStream
    .format("parquet")
    .option(
        "path",
        "./data/bronze/billing_events"
    )
    .option(
        "checkpointLocation",
        "./checkpoints/billing_events"
    )
    .outputMode("append")
    .start()
)


# ==================================================
# Keep Streams Running
# ==================================================

spark.streams.awaitAnyTermination()
