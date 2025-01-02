## ------------ Imports ------------ ##
import sys
sys.path.append("/home/waseem/Documents/Self-Development/git_repos/portfolio/Data Engineering/ecommerce_pipeline/airflow/dags/python_files")
import aws_credentials
import boto3
import os


## ------------ Defaults/Variables ------------ ##
AWS_S3_BUCKET_NAME = aws_credentials.aws_s3_bucket_name
AWS_REGION = aws_credentials.aws_region
AWS_ACCESS_KEY = aws_credentials.aws_access_key
AWS_SECRET_KEY = aws_credentials.aws_secret_access_key

FILEPATH = "downloads"


## ------------ Functions ------------ ##
def delete_s3_file(
        local_filepath=FILEPATH,
        service_name="s3",
        s3_bucket_name=AWS_S3_BUCKET_NAME,
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY):
    """
    This function deletes s3 files with the filepath/directory supplied
    """

    s3_client = boto3.client(
        service_name=service_name,
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    for file in local_filepath:
        s3_client.delete_object(bucket=s3_bucket_name, key=file)
