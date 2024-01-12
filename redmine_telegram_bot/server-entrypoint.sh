#!/bin/sh

TIMEOUT=30
start_time=$(date +%s)

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
    current_time=$(date +%s)
    elapsed_time=$((current_time - start_time))

    if [ $elapsed_time -ge $TIMEOUT ]; then
        echo "Ошибка: Превышено время ожидания. Не удалось установить соединение в течение $TIMEOUT секунд."
        exit 1
    fi

    echo "Ожидание подключения к PostgreSQL. Прошло времени: $elapsed_time секунд."
    sleep 0.1
done

echo "Соединение успешно установлено с PostgreSQL."

# Apply database migrations
echo "Applying database migrations ..."
python manage.py makemigrations

until python manage.py migrate; do
  echo "Waiting for db to be ready..."
  sleep 2
done

# Collecting static
until python manage.py collectstatic --noinput; do
  echo "Collecting static ..."
  sleep 2
done

python manage.py initadmin

# Start server
echo "Starting server ..."
gunicorn redmine_telegram_bot.wsgi:application --bind 0.0.0.0:8000 & python manage.py runpolling
