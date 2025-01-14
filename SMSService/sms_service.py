import pika
import json
import logging
from twilio.rest import Client
from flask import Flask

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def send_sms(to_number, content):
    twilio_client = Client('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN')
    try:
        message = twilio_client.messages.create(
            body=content,
            from_='your_twilio_number',
            to=to_number
        )
        logging.info(f'SMS уведомление отправлено на {to_number}')
    except Exception as e:
        logging.error(f'Ошибка отправки SMS: {e}')

def callback(ch, method, properties, body):
    data = json.loads(body)
    if data['type'] == 'sms':
        send_sms('+12345', data['content'])
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_sms_service():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='notification_queue', durable=True)
    channel.basic_consume(queue='notification_queue', on_message_callback=callback)
    logging.info('SMS Сервис запущен')
    channel.start_consuming()

if __name__ == '__main__':
    start_sms_service()
