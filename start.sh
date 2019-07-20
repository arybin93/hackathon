#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput --verbosity 0

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# run server
python manage.py runserver 0.0.0.0:8000
