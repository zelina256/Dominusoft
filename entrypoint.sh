#!/bin/sh

echo "Waiting for mysql..."

while ! nc -z 127.0.0.1 3306; do
  sleep 0.1
done

echo "mysql started"

python manage.py migrate

exec "$@"
