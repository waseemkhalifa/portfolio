## ------------------------ Imports ------------------------ ##
import sys
sys.path.append("/home/waseem/Documents/Self-Development/git_repos/portfolio/Data Engineering/ecommerce_pipeline_pyspark/airflow/dags/python_files/ecommerce_dataset_generator/src")

from faker import Faker 
from faker.providers import DynamicProvider



## ------------------------ Defaults/Variables ------------------------ ##
fake = Faker("en_GB")

product_provider = DynamicProvider(
    provider_name="product_category",
    elements=["t-shirt", "shirt", "jeans", "hat", "shoes", "blazer", "suit",
              "shorts", "belt", "socks"],
)
fake.add_provider(product_provider)



## ------------------------ Functions ------------------------ ##

def fake_product_prices(product_category) -> float:
    """ 
    Generates a random product price based on the product category. 
    """

    product_price = fake.pyfloat(right_digits=2, 
                                 positive=True, 
                                 min_value=10, 
                                 max_value=60) if product_category == "t-shirt" \
                        else fake.pyfloat(right_digits=2, 
                                          positive=True, 
                                          min_value=30, 
                                          max_value=90) if product_category == "shirt" \
                        else fake.pyfloat(right_digits=2, 
                                          positive=True, 
                                          min_value=40, 
                                          max_value=270) if product_category == "jeans" \
                        else fake.pyfloat(right_digits=2, 
                                          positive=True, 
                                          min_value=5, 
                                          max_value=30) if product_category == "hat" \
                        else fake.pyfloat(right_digits=2, 
                                          positive=True, 
                                          min_value=30, 
                                          max_value=200) if product_category == "shoes" \
                        else fake.pyfloat(right_digits=2, 
                                          positive=True, 
                                          min_value=50, 
                                          max_value=90) if product_category == "blazer" \
                        else fake.pyfloat(right_digits=2, 
                                          positive=True, 
                                          min_value=80, 
                                          max_value=400) if product_category == "suit" \
                        else fake.pyfloat(right_digits=2, 
                                          positive=True, 
                                          min_value=10, 
                                          max_value=20) if product_category == "shorts" \
                        else fake.pyfloat(right_digits=2, 
                                          positive=True, 
                                          min_value=5, 
                                          max_value=35) if product_category == "belt" \
                        else fake.pyfloat(right_digits=2, 
                                          positive=True, 
                                          min_value=1, 
                                          max_value=5) if product_category == "socks" \
                        else 0
    
    return product_price


def fake_product() -> list:
    """ 
    Generates a json object with product data
    """

    product_id = fake.uuid4()
    product_category = fake.product_category()
    product_price = fake_product_prices(product_category)

    product = {
        "product_id": product_id,
        "product_category":product_category,
        "product_price":"{:.2f}".format(product_price)
    }
        

    return product
