import pika
import json
import logging
import smtplib
from email.mime.text import MIMEText
from prometheus_flask_exporter import PrometheusMetrics
from flask import Flask

# Настройка логирования
logging.basicConfig(
    filename='log/email_service.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
metrics = PrometheusMetrics(app)

def send_email(to_email, content):
    msg = MIMEText(content)
    msg['Subject'] = 'Notification'
    msg['From'] = 'your_email@example.com'
    msg['To'] = to_email

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login('your_email@example.com', 'your_password')
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
        logging.info(f'Email sent to {to_email}')
    except Exception as e:
        logging.error(f'Error sending email: {e}')

def callback(ch, method, properties, body):
    data = json.loads(body)
    if data['type'] == 'email':
        send_email('recipient@example.com', data['content'])
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_email_service():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='notification_queue', durable=True)
    channel.basic_consume(queue='notification_queue', on_message_callback=callback)
    logging.info('Email Service started and waiting for messages...')
    channel.start_consuming()

if __name__ == '__main__':
    start_email_service()