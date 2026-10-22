from kafka import KafkaProducer
from faker import Faker

import json
import random
import time
import uuid

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

event_types = [
    "signup",
    "call",
    "data_usage",
    "upgrade",
    "bill",
    "churn"
]

while True:

    event = {

        "event_id": str(uuid.uuid4()),

        "customer_id": random.randint(1000, 9999),

        "event_type": random.choice(event_types),

        "value": round(random.uniform(1, 100), 2),

        "event_timestamp": fake.iso8601()
    }

    producer.send(
        "customer-events",
        event
    )

    print(event)

    time.sleep(1)
