from aiokafka import AIOKafkaProducer
from json import dumps


async def send_email_to_kafka(email: str, name: str) -> bool:
    producer = AIOKafkaProducer(bootstrap_servers=['localhost:9092'],
                                value_serializer=lambda x: dumps(x).encode('utf-8'),
                                acks='all',
                                request_timeout_ms=10000)
    message = {
        'email': email,
        'name': name
    }
    await producer.start()
    try:
        await producer.send_and_wait(topic='emails', value=message)
        return True
    except Exception as e:
        print(f"Failed to send message to Kafka: {e}")
        return False
    finally:
        await producer.stop()
