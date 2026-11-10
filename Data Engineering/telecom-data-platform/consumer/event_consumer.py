import json

from kafka import KafkaConsumer
from kafka.serializer import Deserializer


class JsonDeserializer(Deserializer):
    def deserialize(self, topic, headers=None, data=None):
        if data is None:
            # Support both invocation signatures used by kafka-python.
            data = headers

        if data is None:
            return None

        return json.loads(data.decode("utf-8"))


def run_consumer(topic: str, output_path: str) -> None:
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        value_deserializer=JsonDeserializer()
    )

    try:
        with open(output_path, "a", encoding="utf-8") as file:
            for message in consumer:
                file.write(json.dumps(message.value) + "\n")
                file.flush()

    except KeyboardInterrupt:
        print("\nStopping Kafka consumer...")

    finally:
        consumer.close()
        print("Kafka consumer stopped successfully.")
