import pika
import json
import logging
from flask import Flask, request
from prometheus_client import Counter, Histogram, start_http_server
import time

app = Flask(__name__)

# Мониторинг
notification_counter = Counter('notifications_total', 'Количество уведомлений')
notification_time = Histogram('notification_processing_seconds', 'Время обработки уведомлений')
notification_failures = Counter('notification_failures_total', 'Количество неудачных уведомлений')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
@app.route('/send_notification', methods=['GET'])
def send_notification():
    data = request.json
    message_type = data.get('type')
    message_content = data.get('content')

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='notification_queue', durable=True)

    message = json.dumps({'type': message_type, 'content': message_content})
    start = time.time()
    try:
        channel.basic_publish(exchange='', routing_key='notification_queue', body=message)
        logging.info(f'Сообщение отправлено в очередь: {message}')
        notification_counter.inc()
        notification_time.observe(time.time() - start)
        return 'Уведомление отправлено', 200
    except Exception as e:
        logging.error(f'Не удалось отправить сообщение: {e}')
        notification_failures.inc()
        return 'Не удалось отправить сообщение', 500
    finally:
        connection.close()

if __name__ == '__main__':
    start_http_server(5001)
    app.run(host='0.0.0.0', port=5000)
