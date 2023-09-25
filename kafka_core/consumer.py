import json
import logging
import os

from dotenv import load_dotenv
from enums import KafkaTopic
from handlers import user_registration_handler
from kafka import KafkaConsumer

load_dotenv()

bootstrap_servers = os.getenv("KAFKA_API_URI")


def deserialize_message(message: bytes) -> dict:
    return json.loads(message.decode("utf-8"))


kafka_topic_handlers = {
    KafkaTopic.USER_REGISTRATION: user_registration_handler,
}


topics = [KafkaTopic.USER_REGISTRATION]  # Use topic that you need here
consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers, value_deserializer=deserialize_message)

logger = logging.getLogger(__name__)


def consume_messages(topics_list: list[KafkaTopic]):
    consumer.subscribe([topic.value for topic in topics_list])

    while True:
        try:
            for message in consumer:
                topic_name = KafkaTopic(message.topic)
                topic_handler = kafka_topic_handlers.get(topic_name)
                if topic_handler:
                    print(f"Received message for topic {topic_name}: {message.value}")
                    topic_handler.delay(message.value)
                    print("Hello, i am listening topics from api-gateway service")
        except Exception as exc:
            logger.exception("An error occurred while consuming messages", exc_info=exc)


if __name__ == "__main__":
    consume_messages(topics)
