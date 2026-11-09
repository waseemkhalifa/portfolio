from kafka import KafkaConsumer
from kafka.serializer import Deserializer
import json


class JsonDeserializer(Deserializer):

    def deserialize(self, topic, headers=None, data=None):
        # Support both invocation signatures used by kafka-python
        if data is None:
            data = headers

        if data is None:
            return None

        return json.loads(data.decode("utf-8"))


consumer = KafkaConsumer(
    "customer-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=JsonDeserializer()
)


# Open the output file once

try:
    with open("data/customer_events.jsonl", "a", encoding="utf-8") as file:
        for message in consumer:
            file.write(json.dumps(message.value) + "\n")
            file.flush()

except KeyboardInterrupt:
    print("\nStopping Kafka consumer...")

finally:
    consumer.close()
    print("Kafka consumer stopped successfully.")

