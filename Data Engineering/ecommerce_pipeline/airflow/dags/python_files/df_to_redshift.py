## ------------ Imports ------------ ##
import sys
sys.path.append("/home/waseem/Documents/Self-Development/git_repos/portfolio/Data Engineering/ecommerce_pipeline/airflow/dags/python_files")
import aws_credentials
import boto3

import redshift_connector
import awswrangler as wr



## ------------ Defaults/Variables ------------ ##
AWS_S3_BUCKET_NAME = aws_credentials.aws_s3_bucket_name
AWS_REGION = aws_credentials.aws_region
AWS_ACCESS_KEY = aws_credentials.aws_access_key
AWS_SECRET_KEY = aws_credentials.aws_secret_access_key

AWS_REDSHIFT_HOST = aws_credentials.aws_redshift_host
AWS_REDSHIFT_DB = aws_credentials.aws_redshift_database
AWS_REDSHIFT_USER = aws_credentials.aws_redshift_user
AWS_REDSHIFT_PASSWORD = aws_credentials.aws_redshift_password



## ------------ Functions ------------ ##
def upload_df_to_redshift(
        df,
        target_redshift_table,
        target_redshift_schema,
        redshift_write_mode="append",
        s3_bucket_name=AWS_S3_BUCKET_NAME,
        aws_region=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        target_redshift_host=AWS_REDSHIFT_HOST,
        target_redshift_db=AWS_REDSHIFT_DB,
        target_redshift_user=AWS_REDSHIFT_USER,
        target_redshift_password=AWS_REDSHIFT_PASSWORD
    ):
    """
    Uploads a DataFrame to Redshift and stores as a table
    """

    # Credentials for the S3 bucket
    # We will use S3 to temp store the DF before exporting to Redshift
    s3_client = boto3.client(
        service_name="s3",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    
    # Credentials and connector for Redshift
    redshift_conn = redshift_connector.connect(
        host=target_redshift_host,
        database=target_redshift_db,
        user=target_redshift_user,
        password=target_redshift_password
    )

    wr.redshift.copy(
        boto3_session=s3_client,
        df = df, # pandas DataFrame
        path = f"s3://{s3_bucket_name}/filename.parquet", # Temp S3 path
        con = redshift_conn, # Redshift connection
        table = target_redshift_table, # Target table
        schema = target_redshift_schema, # Target schema in Redshift
        mode = redshift_write_mode # overwrite or append
    )
