# notification-service
Способ запуска и проверки: 

Запустите все сервисы: Перейдите в корень проекта и выполните команду docker-compose up --build

Проверьте доступность RabbitMQ: http://localhost:15672 (логин: guest, пароль: guest)

Отправьте уведомление: С помощью Postman выполните POST запрос на http://localhost:5000/send_notification с JSON-данными: json { "type": "email", "name@gmail.com", "content": "Привет!" }

Проверьте доступность RabbitMQ: http://localhost:15672 (логин: guest, пароль: guest)
Вы можете открыть интерфейс Prometheus по адресу http://localhost:9090 для мониторинга метрик (например, по запросу notifications_total можно увидеть количество отправленных уведомлений).
