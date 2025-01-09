import pika
import json
import logging
from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/send_notification', methods=['POST'])
def send_notification():
    data = request.json
    message_type = data.get('type')
    message_content = data.get('content')

    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='notification_queue', durable=True)

    message = json.dumps({'type': message_type, 'content': message_content})

    try:
        channel.basic_publish(exchange='', routing_key='notification_queue', body=message)
        logging.info(f'Сообщение отправлено в очередь: {message}')
        return 'Notification sent', 200
    except Exception as e:
        logging.error(f'Не удалось отправить сообщение: {e}')
        return 'Не удалось отправить сообщение', 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
