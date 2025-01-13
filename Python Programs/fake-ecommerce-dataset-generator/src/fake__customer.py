## ------------------------ Imports ------------------------ ##
import random

from faker import Faker 
from faker.providers import DynamicProvider



## ------------------------ Defaults/Variables ------------------------ ##
fake = Faker()


## ------------------------ Functions ------------------------ ##
def fake_customer(faker_seed:int) -> dict:
    """ 
    Generates a json object with user data
    """

    Faker.seed(faker_seed)
        
    gender = random.choice(["m","f"])
    customer_id = fake.uuid4()
    customer_prefix = fake.prefix_male() if gender=='m' else fake.prefix_female()
    first_name = fake.first_name_male() if gender=='m' else fake.first_name_female()
    last_name = fake.last_name_male() if gender=='m' else fake.last_name_female()

    email_seperator = random.choice([".","_","-",""])
    customer_email = f"{first_name}{email_seperator}{last_name}@{fake.free_email_domain()}".lower()

    customer = {"customer_id": customer_id,
                "customer_prefix":customer_prefix,
                "first_name":first_name,
                "last_name":last_name,
                "customer_email":customer_email}
    

    return customer

