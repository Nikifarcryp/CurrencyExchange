from kafka import KafkaProducer
from json import dumps


def send_email_to_kafka(email: str, name: str) -> bool:
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x: dumps(x).encode('utf-8'),
                             acks='all',
                             retries=5,
                             request_timeout_ms=10000)
    message = {
        'email': email,
        'name': name
    }
    try:
        future = producer.send(topic='emails', value=message)
        future.add_callback(
            lambda metadata: print(f"✅ Successfully sent in {metadata.topic} (place {metadata.partition})"))
        future.add_errback(lambda error: print(f"❌ Send error to Kafka: {error}"))
        future.get(timeout=10)
        return True
    except Exception as e:
        print(f"Failed to send message to Kafka: {e}")
        return False
    finally:
        producer.close()
