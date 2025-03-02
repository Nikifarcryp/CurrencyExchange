import asyncio
from aiokafka import AIOKafkaConsumer
import json
from dotenv import load_dotenv
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

gmail_user_from = os.getenv("GMAIL_LOGIN")
gmail_password_from = os.getenv("GMAIL_PASSWORD")


def build_and_send_email(gmail_user_to, name):
    msg = MIMEMultipart()
    msg["From"] = gmail_user_from
    msg["To"] = gmail_user_to
    msg["Subject"] = "Thank you for joining us!"
    body = f"{name}, we appreciate you interest for us and our Exchanger. Thank you a lot!"
    msg.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(gmail_user_from, gmail_password_from)
        server.send_message(msg)
        server.quit()
        print("Message successfully sent!")
    except Exception as e:
        print(f"Error: {e}")


async def consume_emails():
    consumer = AIOKafkaConsumer('emails',
                                bootstrap_servers='localhost:9092',
                                value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    await consumer.start()
    print("🔄 Waiting for messages from Kafka ...")
    while True:
        try:
            async for record in consumer:
                print(f"📩 Received message: {record.value}")
                build_and_send_email(record.value['email'], record.value['name'])
        except Exception as e:
            print(f"❌ Processing error: {e}")


asyncio.run(consume_emails())
