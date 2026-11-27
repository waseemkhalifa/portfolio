## ------------ Imports ------------ ##
import random

from datetime import datetime, timedelta

from dataclasses import dataclass, asdict

from faker import Faker 
from faker.providers import DynamicProvider



## ------------ Defaults/Variables ------------ ##
TRANSACTION_MIN = 1
TRANSACTION_MAX = 9
CURRENT_DATETIME = datetime.now().strftime("%Y-%m-%d %H-%M-%S")


fake = Faker("en_GB")

product_provider = DynamicProvider(
    provider_name="product_category",
    elements=["t-shirt", "shirt", "jeans", "hat", "shoe"],
)
fake.add_provider(product_provider)



## ------------ Classes ------------ ##
@dataclass
class Transaction:
    transaction_id:str
    transaction_datetime:str
    user_id:str 
    user_prefix:str
    first_name:str
    last_name:str 
    user_email:str
    product_id:str
    product_category:str



## ------------ Functions ------------ ##
def get_transactions(TRANSACTION_MIN, TRANSACTION_MAX) -> list[Transaction]:
    """
    Creates fake transactions and stores them as dataclass objects in a List
    """

    transactions:list[Transaction] = []

    for x in range(random.randint(TRANSACTION_MIN, TRANSACTION_MAX)):
        transaction:Transaction = Transaction(
            transaction_id = fake.uuid4(),
            transaction_datetime = CURRENT_DATETIME,
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
