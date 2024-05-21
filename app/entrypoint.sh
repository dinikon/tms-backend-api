#!/bin/sh

# Сбор статических файлов
python manage.py collectstatic --noinput

# Запуск приложения
exec "$@"
