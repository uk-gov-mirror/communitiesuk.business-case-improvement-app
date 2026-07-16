#!/bin/sh
set -e

echo "Waiting for database to be ready..."
until python - <<'PY'
import os
import psycopg

psycopg.connect(
		dbname=os.environ["DB_NAME"],
		user=os.environ["DB_USER"],
		password=os.environ["DB_PASSWORD"],
		host=os.environ["DB_HOST"],
		port=os.environ["DB_PORT"],
		connect_timeout=2,
).close()
PY
do
	echo "Database unavailable, retrying in 1s..."
	sleep 1
done

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec "$@"
