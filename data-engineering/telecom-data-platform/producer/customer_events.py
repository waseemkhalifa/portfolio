import json
import random
import time
import uuid

from faker import Faker
from kafka import KafkaProducer

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

event_types = [
    "signup",
    "package_upgrade",
    "package_downgrade",
    "add_on_purchase",
    "contract_renewal",
    "customer_support_contact",
    "customer_churn"
]

packages = [
    "Basic",
    "Standard",
    "Premium",
    "Unlimited"
]

channels = [
    "web",
    "mobile_app",
    "call_centre",
    "retail_store"
]


def generate_event():
    event_type = random.choice(event_types)

    event = {
        "event_id": str(uuid.uuid4()),
        "customer_id": random.randint(10, 99),
        "event_type": event_type,
        "event_timestamp": fake.iso8601(),
        "channel": random.choice(channels)
    }

    if event_type == "signup":
        event.update({
            "package_name": random.choice(packages),
            "monthly_charge": round(random.uniform(15, 60), 2),
            "contract_length_months": random.choice([12, 18, 24])
        })

    elif event_type == "package_upgrade":
        event.update({
            "old_package": "Standard",
            "new_package": random.choice(["Premium", "Unlimited"]),
            "monthly_charge_increase": round(random.uniform(5, 20), 2)
        })

    elif event_type == "package_downgrade":
        event.update({
            "old_package": random.choice(["Premium", "Unlimited"]),
            "new_package": "Standard",
            "monthly_charge_decrease": round(random.uniform(5, 15), 2)
        })

    elif event_type == "add_on_purchase":
        event.update({
            "add_on_name": random.choice([
                "Extra Data",
                "Roaming Pass",
                "International Calls",
                "Netflix Bundle"
            ]),
            "add_on_cost": round(random.uniform(3, 15), 2)
        })

    elif event_type == "contract_renewal":
        event.update({
            "contract_length_months": random.choice([12, 24, 36]),
            "renewal_discount": round(random.uniform(0, 20), 2)
        })

    elif event_type == "customer_support_contact":
        event.update({
            "case_type": random.choice([
                "billing",
                "technical",
                "network",
                "upgrade"
            ]),
            "resolved_first_contact": random.choice([True, False])
        })

    elif event_type == "customer_churn":
        event.update({
            "churn_reason": random.choice([
                "price",
                "competitor",
                "coverage",
                "customer_service"
            ])
        })

    return event

try:
    while True:
        event = generate_event()

        producer.send(
            "customer-events",
            event
        )

        print(event)

        time.sleep(2)

except KeyboardInterrupt:
    print("\nStopping Kafka producer...")

finally:
    producer.close()
    print("Kafka producer stopped successfully.")
