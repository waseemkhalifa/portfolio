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
    "call_completed",
    "call_dropped",
    "data_session",
    "sms_sent",
    "network_outage",
    "roaming_usage",
    "speed_test"
]

network_types = [
    "4G",
    "5G"
]

regions = [
    "London",
    "Birmingham",
    "Manchester",
    "Leeds",
    "Glasgow",
    "Cardiff",
    "Coventry"
]


def generate_event():
    event_type = random.choice(event_types)

    event = {
        "event_id": str(uuid.uuid4()),
        "customer_id": random.randint(1000, 9999),
        "event_type": event_type,
        "region": random.choice(regions),
        "network_type": random.choice(network_types),
        "event_timestamp": fake.iso8601()
    }

    if event_type == "call_completed":
        event.update({
            "call_duration_seconds": random.randint(10, 3600)
        })

    elif event_type == "call_dropped":
        event.update({
            "call_duration_seconds": random.randint(1, 600),
            "signal_strength": random.randint(1, 5)
        })

    elif event_type == "data_session":
        event.update({
            "data_used_mb": round(random.uniform(10, 5000), 2),
            "session_duration_minutes": random.randint(1, 180)
        })

    elif event_type == "sms_sent":
        event.update({
            "message_count": random.randint(1, 10)
        })

    elif event_type == "network_outage":
        event.update({
            "affected_customers": random.randint(100, 10000),
            "outage_duration_minutes": random.randint(5, 240)
        })

    elif event_type == "roaming_usage":
        event.update({
            "country": random.choice([
                "Spain",
                "France",
                "Germany",
                "Italy",
                "USA"
            ]),
            "data_used_mb": round(random.uniform(10, 2000), 2)
        })

    elif event_type == "speed_test":
        event.update({
            "download_speed_mbps": round(random.uniform(5, 500), 2),
            "upload_speed_mbps": round(random.uniform(1, 100), 2),
            "latency_ms": random.randint(5, 150)
        })

    return event


try:
    while True:
        event = generate_event()

        producer.send(
            "network-events",
            event
        )

        print(event)

        time.sleep(2)

except KeyboardInterrupt:
    print("\nStopping Kafka producer...")

finally:
    producer.close()
    print("Kafka producer stopped successfully.")
