#!/bin/bash

set -e

echo "Waiting for MySQL to start..."

# Python skript orqali MySQL tayyorligini tekshirish
until python -c "import sys; import MySQLdb; 
try:
    conn = MySQLdb.connect(
        host='$MYSQL_HOST',
        user='$MYSQL_USER',
        passwd='$MYSQL_PASSWORD',
        db='$MYSQL_DATABASE'
    )
    conn.close()
except Exception as e:
    sys.exit(1)
"; do
  echo "Waiting for database..."
  sleep 2
done

echo "MySQL is up - executing commands..."

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Creating superuser..."
python manage.py createadmin

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Starting the app
echo "Starting application..."
#python app.py  # app.py faylini to'g'ri joylashgan joyini ko'rsatish

exec "$@"
