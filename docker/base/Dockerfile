# Используем официальный образ Python как базовый
FROM python:3.12-slim
LABEL authors="inikon"

# Устанавливаем рабочую директорию в контейнере
WORKDIR /tms-app

# Копируем зависимости
COPY ./app/requirements.txt /tms-app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /tms-app/requirements.txt

# Копируем остальные файлы проекта
COPY ./app /tms-app/

# Копируем entrypoint.sh
COPY ./app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Указываем порт, который будет слушать контейнер
EXPOSE 8000

# Используем entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Запускаем Django-приложение
CMD ["gunicorn", "app.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--workers", "4", "--threads", "4", "--worker-tmp-dir", "/dev/shm", "--log-file", "-", "--bind", "0.0.0.0:8000"]