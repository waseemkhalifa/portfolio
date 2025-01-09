## ------------------------ Imports ------------------------ ##
import random
import json

from faker import Faker 
from faker.providers import DynamicProvider



## ------------------------ Defaults/Variables ------------------------ ##
Faker.seed(0)
fake = Faker("en_GB")

product_provider = DynamicProvider(
    provider_name="product_category",
    elements=["t-shirt", "shirt", "jeans", "hat", "shoes", "blazer", "suit",
              "shorts", "belt", "socks"],
)
fake.add_provider(product_provider)



## ------------------------ Functions ------------------------ ##
def fake_products(num_of_products:int) -> dict:

    products:list[dict] = []

    for x in range(0, num_of_products):
        products.append({"product_id": fake.uuid4(), 
                         "product_category":fake.product_category()})

    return products
