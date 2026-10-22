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

    print(
        message.value
    )
