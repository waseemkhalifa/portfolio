from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    lower,
    current_timestamp,
    col
)

# ==================================================
# Create Spark Session
# ==================================================

spark = (
    SparkSession.builder
    .appName("customer-events-silver-layer")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# ==================================================
# Read Bronze Data
# ==================================================

bronze_df = spark.read.parquet(
    "./data/bronze/customer_events"
)

# ==================================================
# Data Quality Rules
# ==================================================

silver_df = bronze_df.filter(
    col("customer_id").isNotNull()
)

silver_df = silver_df.filter(
    col("event_id").isNotNull()
)


# ==================================================
# Standardise Event Types
# ==================================================

silver_df = silver_df.withColumn(
    "event_type",
    lower(col("event_type"))
)

# ==================================================
# Add Audit Columns
# ==================================================

silver_df = silver_df.withColumn(
    "processed_timestamp",
    current_timestamp()
)

# ==================================================
# Preview Data
# ==================================================

print("\nSilver Customer Events Preview\n")

silver_df.show(
    truncate=False
)

# ==================================================
# Write Silver Layer
# ==================================================

silver_df.write \
    .mode("overwrite") \
    .parquet(
        "./data/silver/customer_events"
    )

print(
    "\nCustomer Silver Layer Created Successfully\n"
)
