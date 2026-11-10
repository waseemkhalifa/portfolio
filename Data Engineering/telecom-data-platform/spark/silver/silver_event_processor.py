from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, current_timestamp, lower


def process_silver_events(
    event_name: str,
    required_columns: tuple[str, ...] = ("event_id", "customer_id"),
) -> DataFrame:
    """Create and write a silver dataset for the named event type."""
    app_name = f"{event_name.replace('_', '-')}-silver-layer"
    event_label = event_name.removesuffix("_events").replace("_", " ").title()
    bronze_path = f"./data/bronze/{event_name}"
    silver_path = f"./data/silver/{event_name}"

    spark = SparkSession.builder.appName(app_name).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    silver_df = spark.read.parquet(bronze_path)

    for column_name in required_columns:
        silver_df = silver_df.filter(col(column_name).isNotNull())

    silver_df = silver_df.withColumn("event_type", lower(col("event_type")))
    silver_df = silver_df.withColumn("processed_timestamp", current_timestamp())

    print(f"\nSilver {event_label} Events Preview\n")
    silver_df.show(truncate=False)

    silver_df.write.mode("overwrite").parquet(silver_path)

    print(f"\n{event_label} Silver Layer Created Successfully\n")
    return silver_df
