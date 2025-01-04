## ------------ Imports ------------ ##
import pandas as pd 
import redshift_connector
redshift_connector.paramstyle = "named"
import awswrangler as wr
import boto3

import sys
sys.path.append("/home/waseem/Documents/Self-Development/git_repos/portfolio/Data Engineering/ecommerce_pipeline/airflow/dags/python_files")
import aws_credentials

import transactions_json_to_df as j2f



## ------------ Defaults/Variables ------------ ##
AWS_S3_BUCKET_NAME = aws_credentials.aws_s3_bucket_name
AWS_ACCESS_KEY = aws_credentials.aws_access_key
AWS_SECRET_KEY = aws_credentials.aws_secret_access_key

AWS_REDSHIFT_HOST = aws_credentials.aws_redshift_host
AWS_REDSHIFT_USER = aws_credentials.aws_redshift_user
AWS_REDSHIFT_PASSWORD = aws_credentials.aws_redshift_password



## ------------ Functions ------------ ##
def dataframe_to_redshift(transaction_json_list,
                          redshift_target_db,
                          redshift_target_schema,
                          redshift_target_table,
                          write_mode="append", # overwrite or append
                          s3_bucket=AWS_S3_BUCKET_NAME,
                          aws_access_key=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY,
                          aws_redshift_host=AWS_REDSHIFT_HOST,
                          aws_redshift_user=AWS_REDSHIFT_USER,
                          aws_redshift_password=AWS_REDSHIFT_PASSWORD
                          ):

    df = j2f.transactions_json_to_dataframe(lst=transaction_json_list)

    s3_session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key
    )

    redshift_conn = redshift_connector.connect(
        host=aws_redshift_host,
        database=redshift_target_db,
        user=aws_redshift_user,
        password=aws_redshift_password
    )

    wr.s3.delete_objects(f"s3://{s3_bucket}/filename.csv")

    wr.redshift.copy(
        boto3_session=s3_session,
        df = df,
        # path = f"s3://{s3_bucket}/filename.parquet", # temp S3 path
        path = f"s3://{s3_bucket}/filename.csv", # temp S3 path
        con = redshift_conn,
        table = redshift_target_table, # target table
        schema = redshift_target_schema, # target database/schema in redshift
        mode = write_mode # overwrite or append
    )
