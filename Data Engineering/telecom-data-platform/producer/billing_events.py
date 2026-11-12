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
    "bill_generated",
    "bill_paid",
    "payment_failed",
    "direct_debit_setup",
    "direct_debit_cancelled",
    "refund_issued",
    "late_payment"
]

payment_methods = [
    "direct_debit",
    "card",
    "bank_transfer"
]

currencies = ["GBP"]


def generate_event():
    event_type = random.choice(event_types)

    event = {
        "event_id": str(uuid.uuid4()),
        "customer_id": random.randint(10, 99),
        "billing_account_id": random.randint(10000, 99999),
        "event_type": event_type,
        "event_timestamp": fake.iso8601(),
        "currency": "GBP"
    }

    if event_type == "bill_generated":
        event.update({
            "bill_id": str(uuid.uuid4()),
            "bill_amount": round(random.uniform(20, 150), 2),
            "bill_period": fake.date(pattern="%Y-%m"),
            "due_date": str(fake.future_date())
        })

    elif event_type == "bill_paid":
        event.update({
            "bill_id": str(uuid.uuid4()),
            "payment_amount": round(random.uniform(20, 150), 2),
            "payment_method": random.choice(payment_methods)
        })

    elif event_type == "payment_failed":
        event.update({
            "bill_id": str(uuid.uuid4()),
            "attempted_amount": round(random.uniform(20, 150), 2),
            "failure_reason": random.choice([
                "insufficient_funds",
                "expired_card",
                "bank_rejection",
                "account_closed"
            ])
        })

    elif event_type == "direct_debit_setup":
        event.update({
            "bank_name": fake.company(),
            "mandate_id": str(uuid.uuid4())
        })

    elif event_type == "direct_debit_cancelled":
        event.update({
            "cancellation_reason": random.choice([
                "customer_request",
                "bank_request",
                "account_closed"
            ])
        })

    elif event_type == "refund_issued":
        event.update({
            "refund_amount": round(random.uniform(5, 50), 2),
            "refund_reason": random.choice([
                "billing_error",
                "service_outage",
                "goodwill_gesture"
            ])
        })

    elif event_type == "late_payment":
        event.update({
            "bill_id": str(uuid.uuid4()),
            "days_overdue": random.randint(1, 60),
            "outstanding_balance": round(random.uniform(20, 200), 2)
        })

    return event


try:
    while True:
        event = generate_event()

        producer.send(
            "billing-events",
            event
        )

        print(event)

        time.sleep(2)

except KeyboardInterrupt:
    print("\nStopping Kafka producer...")

finally:
    producer.close()
    print("Kafka producer stopped successfully.")
