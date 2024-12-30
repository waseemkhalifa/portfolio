## ------------ Imports ------------ ##
import sys
sys.path.append("/home/waseem/Documents/Self-Development/git_repos/portfolio/Data Engineering/ecommerce_pipeline/airflow/dags/python_files")
import aws_credentials
import boto3


## ------------ Defaults/Variables ------------ ##
AWS_S3_BUCKET_NAME = aws_credentials.aws_s3_bucket_name
AWS_REGION = aws_credentials.aws_region
AWS_ACCESS_KEY = aws_credentials.aws_access_key
AWS_SECRET_KEY = aws_credentials.aws_secret_access_key



## ------------ Functions ------------ ##
def save_json_file_to_s3(
        local_file, 
        file_name,
        service_name="s3",
        s3_bucket_name=AWS_S3_BUCKET_NAME,
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY):
    """
    Exports local JSON file to S3 bucket
    """
    
    s3_client = boto3.client(
        service_name=service_name,
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    response = s3_client.upload_file(local_file, s3_bucket_name, file_name)
