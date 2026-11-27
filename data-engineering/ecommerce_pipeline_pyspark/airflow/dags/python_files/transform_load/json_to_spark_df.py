## ------------ Imports ------------ ##
import os
from pyspark.sql.types import StructType
from pyspark.sql import SparkSession



## ------------ Defaults/Variables ------------ ##
# Create a SparkSession
spark = SparkSession.builder.appName("dim_products").getOrCreate()



## ------------ Functions ------------ ##
def spark_read_json_as_df(directory):
    """ Returns a Spark DataFrame for json files in a directory """
    
    # Create empty spark dataframe
    df = spark.createDataFrame([], StructType([]))

    # This retrieves all the files in the directory
    for file in os.listdir(directory):
        # If file is a json, construct it's full path and open it
        if file.endswith(".json"):
            # New data as Spark DataFrame
            temp_df = spark.read.json(os.path.join(directory, file))
            # Overwrite original dataframe
            if df.isEmpty():
                df = temp_df
            else:
                df = df.unionByName(temp_df)
    return df
