## ------------ Imports ------------ ##
import random
from datetime import datetime

import fake__customer as fc
import fake__product as fp

from faker import Faker 
from faker.providers import DynamicProvider
fake = Faker("en_GB")



## ------------ Functions ------------ ##

def get_transactions(customer_seed:int, 
                     product_seed:int, 
                     transaction_min:int, 
                     transaction_max:int) -> list[dict]:
    """
    Creates fake transactions and stores them as json objects in a list
    """

    customers:list[dict] = []
    for cust in range(1, 100):
        customers.append(fc.fake_customer(customer_seed))
    
    products:list[dict] = []
    for prod in range(1, 100):
        products.append(fp.fake_product(product_seed))


    transactions:list[dict] = []

    for x in range(random.randint(transaction_min, transaction_max)):
        
        random.seed(random.randint(1,100))
        customer = random.choice(customers)
        product = random.choice(products)

        transaction:dict = {
            "transaction_id":fake.uuid4(),
            "transaction_datetime":datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
            "customer": customer,
            "product": product
        }
            
        transactions.append(transaction)

    return transactions
