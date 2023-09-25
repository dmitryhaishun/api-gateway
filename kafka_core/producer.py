import json
import os
from typing import Any

from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv()

bootstrap_servers = os.getenv("KAFKA_API_URI")


def serialize_message(value: Any) -> bytes:
    return json.dumps(value).encode("utf-8")


def send_to_kafka(topic: str, message: Any) -> None:
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=serialize_message)
    producer.send(topic, message)
    producer.flush()
    producer.close()
