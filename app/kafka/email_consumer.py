from kafka import KafkaConsumer
import json
from dotenv import load_dotenv
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

gmail_user_from = os.getenv("GMAIL_LOGIN")
gmail_password_from = os.getenv("GMAIL_PASSWORD")

consumer = KafkaConsumer('emails',
                         bootstrap_servers='localhost:9092',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))


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





def consume_emails():
    print("🔄 Waiting for messages from Kafka ...")
    while True:
        records = consumer.poll(timeout_ms=1000)
        if records:
            try:
                for _, batch in records.items():
                    for record in batch:
                        print(f"📩 Recieved message: {record.value}")
                        build_and_send_email(record.value['email'], record.value['name'])
            except Exception as e:
                print(f"❌ Processing error: {e}")


consume_emails()
