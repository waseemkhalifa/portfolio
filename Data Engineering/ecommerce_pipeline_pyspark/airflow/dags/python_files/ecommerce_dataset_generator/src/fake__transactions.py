## ------------ Imports ------------ ##
import sys
sys.path.append("/home/waseem/Documents/Self-Development/git_repos/portfolio/Data Engineering/ecommerce_pipeline_pyspark/airflow/dags/python_files/ecommerce_dataset_generator/src")

import random
from datetime import datetime

import fake__customer as fc
import fake__product as fp

from faker import Faker 
fake = Faker("en_GB")



## ------------ Functions ------------ ##

def get_transactions(transaction_min:int, 
                     transaction_max:int) -> list[dict]:
    """
    Creates fake transactions and stores them as json objects in a list
    """

    customers:list[dict] = []
    for cust in range(1, 500):
        customers.append(fc.fake_customer())
    
    products:list[dict] = []
    for prod in range(1, 100):
        products.append(fp.fake_product())


    transactions:list[dict] = []

    for x in range(random.randint(transaction_min, transaction_max)):
        
        random.seed(random.randint(1,100))
        customer = random.choice(customers)

        product = []
        for p in range(random.randint(1, 5)):
            product.append(random.choice(products))

        transaction:dict = {
            "transaction_id":fake.uuid4(),
            "transaction_datetime":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer": customer,
            "product": product
        }
            
        transactions.append(transaction)

    return transactions
