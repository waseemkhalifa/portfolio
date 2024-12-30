from faker import Faker 
from faker.providers import DynamicProvider

import json
import random
import boto3

from dataclasses import dataclass, asdict


import os
import sys
sys.path.append("/home/waseem/Documents/Self-Development/git_repos/portfolio/Data Engineering/ecommerce_pipeline/airflow/dags/python_files")
import aws_credentials


fake = Faker("en_GB")

product_provider = DynamicProvider(
    provider_name="product_category",
    elements=["t-shirt", "shirt", "jeans", "hat", "shoe"],
)

fake.add_provider(product_provider)


AWS_S3_BUCKET_NAME = aws_credentials.aws_s3_bucket_name
AWS_REGION = aws_credentials.aws_region
AWS_ACCESS_KEY = aws_credentials.aws_access_key
AWS_SECRET_KEY = aws_credentials.aws_secret_access_key

LOCAL_FILE = "transactions.json"
NAME_FOR_S3_FILE = 'transactions_s3.json'



@dataclass
class Transaction:
    transaction_id:str
    user_id:str 
    user_prefix:str
    first_name:str
    last_name:str 
    user_email:str
    product_id:str
    product_category:str



def get_transactions(tranasactions_min=1, tranasactions_max=3) -> list[Transaction]:
    transactions:list[Transaction] = []

    for x in range(random.randint(tranasactions_min, tranasactions_max)):
        transaction:Transaction = Transaction(
            transaction_id = fake.uuid4(),
            user_id = fake.uuid4(),
            user_prefix = fake.prefix(),
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            user_email = fake.ascii_email(),
            product_id = fake.uuid4(),
            product_category = fake.product_category()
        )
        transactions.append(transaction)

    return transactions


def convert_dataclass_to_json(dataclass_list:list[Transaction]) -> list:
    lst:list = []
    for dataclass in dataclass_list:
        lst.append(asdict(dataclass))
    
    return lst


def save_list_as_json_file(lst:list, file_name=LOCAL_FILE):
    with open(file_name, "w") as fd:
        fd.write(json.dumps(lst))


def save_json_file_to_s3(
        local_file="transactions.json", 
        file_name=NAME_FOR_S3_FILE,
        service_name="s3",
        s3_bucket_name=AWS_S3_BUCKET_NAME,
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY):
    
    s3_client = boto3.client(
        service_name='s3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    response = s3_client.upload_file(LOCAL_FILE, 
                                     AWS_S3_BUCKET_NAME, 
                                     file_name)


def get_transactions_load_s3():
    transactions = get_transactions()
    transactions = convert_dataclass_to_json(transactions)
    save_list_as_json_file(transactions)
    save_json_file_to_s3()
