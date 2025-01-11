## ------------------------ Imports ------------------------ ##
import random
import decimal

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

def fake_product_prices(product_category) -> float:
    product_price = 1


def fake_products(num_of_products:int) -> dict:

    products:list[dict] = []

    for x in range(0, num_of_products):

        product_id = fake.uuid4()
        product_category = fake.product_category()

        product_price = random.uniform(10, 60) if product_category == "t-shirt" \
                        else random.uniform(30, 90) if product_category == "shirt" \
                        else random.uniform(40, 270) if product_category == "jeans" \
                        else random.uniform(5, 30) if product_category == "hat" \
                        else random.uniform(30, 200) if product_category == "shoes" \
                        else random.uniform(50, 90) if product_category == "blazer" \
                        else random.uniform(80, 400) if product_category == "suit" \
                        else random.uniform(10, 20) if product_category == "shorts" \
                        else random.uniform(5, 35) if product_category == "belt" \
                        else random.uniform(1, 5) if product_category == "socks" \
                        else 0

        product = {"product_id": product_id,
                   "product_category":product_category,
                   "product_price":"{:.2f}".format(product_price)
                   }
        
        products.append(product)

    return products
