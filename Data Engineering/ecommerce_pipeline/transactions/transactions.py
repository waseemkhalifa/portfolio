from faker import Faker 
from faker.providers import DynamicProvider

import json
import random



fake = Faker("en_GB")


product_provider = DynamicProvider(
    provider_name="product_category",
    elements=["t-shirt", "shirt", "jeans", "hat", "shoe"],
)
fake.add_provider(product_provider)



@dataclass
class Transaction:
    user_id:str 
    user_prefix:str
    first_name:str
    last_name:str 
    user_email:str
    transaction_id:str
    product_id:str
    product_category:str


transactions:list[Transaction] = []

for x in range(random.randint(0, 9)):
    transaction:Transaction = Transaction(
        user_id = fake.uuid4(),
        user_prefix = fake.prefix(),
        first_name = fake.first_name(),
        last_name = fake.last_name(),
        user_email = fake.ascii_email(),
        transaction_id = fake.uuid4(),
        product_id = fake.uuid4(),
        product_category = fake.product_category()
    )
    transactions.append(transaction)

print(json.dumps(transactions))
