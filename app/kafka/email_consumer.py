from kafka import KafkaConsumer
import json
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

gmail_user_from = "pprogovich@gmail.com"
gmail_password_from = "xlabbzmiabxmaqpb"

consumer = KafkaConsumer('email_notifications',
                         bootstrap_servers='localhost:9092',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))


def send_email(gmail_user_to):
    msg = MIMEMultipart()
    msg["From"] = gmail_user_from
    msg["To"] = gmail_user_to
    msg["Subject"] = "Привет от Python!"
    body = "Это тестовое письмо, отправленное через Python."
    msg.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(gmail_user_from, gmail_password_from)
        server.send_message(msg)
        server.quit()
        print("Письмо успешно отправлено!")
    except Exception as e:
        print(f"Ошибка: {e}")



def consume_emails():
    print("🔄 Ожидание сообщений из Kafka...")
    while True:
        message = consumer.poll(timeout_ms=1000)
        try:
            msg = message['email']  # Декодировать не нужно, KafkaConsumer уже делает это
            print(f"📩 Получено сообщение: {msg}")
            send_email(msg['email'])
        except Exception as e:
            print(f"❌ Ошибка обработки сообщения: {e}")


consume_emails()
