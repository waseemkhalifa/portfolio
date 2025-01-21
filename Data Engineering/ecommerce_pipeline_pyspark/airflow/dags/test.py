import pandas as pd 

df = pd.read_parquet("etl/dim_products.parquet")

df.show(10)

