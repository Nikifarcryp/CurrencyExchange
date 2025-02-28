from kafka import KafkaProducer
from json import dumps
import atexit


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'),
                         acks='all',  # Дожидаемся подтверждения от всех реплик
                         retries=5,  # Пробуем повторно, если ошибка
                         request_timeout_ms=10000)


def send_email_to_kafka(email: str):
    message = {
        'email': email
    }
    try:
        future = producer.send(topic='email_notifications', value=message)
        future.get(timeout=10)
        future.add_callback(
            lambda metadata: print(f"✅ Успешно отправлено в {metadata.topic} (раздел {metadata.partition})"))
        future.add_errback(lambda error: print(f"❌ Ошибка при отправке в Kafka: {error}"))
        producer.flush()
        return True
    except Exception as e:
        print(f"Failed to send message to Kafka: {e}")
        return False


atexit.register(lambda: producer.close())