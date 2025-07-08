#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn logomaker.wsgi:application --config gunicorn.conf.py