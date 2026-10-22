from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "customer-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(
        m.decode("utf-8")
    )
)

for message in consumer:

    with open(
        "data/customer_events.jsonl",
        "a"
    ) as file:

        file.write(
            json.dumps(message.value)
            + "\n"
        )
