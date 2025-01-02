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

try:
    os.mkdir("downloads")
    print(f"Directory 'downloads' created successfully.")
except FileExistsError:
    print(f"Directory 'downloads'  already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create 'downloads' .")
except Exception as e:
    print(f"An error occurred: {e}")

FILEPATH = "downloads"


## ------------ Functions ------------ ##
def download_s3_files(
        service_name="s3",
        s3_bucket_name=AWS_S3_BUCKET_NAME,
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        filepath = FILEPATH):
    """
    Downloads S3 files to a local downloads folder
    """
    
    s3_client = boto3.client(
        service_name=service_name,
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    list_files = s3_client.list_objects(Bucket=s3_bucket_name)["Contents"]

    for key in list_files:
        download_file_path = os.path.join(filepath, key["Key"])
        
        s3_client.download_file(
            Bucket = s3_bucket_name,
            Key = key["Key"],
            Filename = download_file_path    
        )
