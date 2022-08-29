#!/usr/bin/env sh

# Apply any pending database migration
python manage.py migrate

# Uncomment to use cron service in microservice backend
# env > /opt/evars.sh
# service cron start >> logs/cron.log 2>&1

# Start server

## Daphne can be used for websocket support
## You will need to install it with this command: pip3 install daphne
#daphne -b 0.0.0.0 -p 8000 microservice.asgi:application

## Serve django trough gunicorn:
gunicorn --bind 0.0.0.0:8000  --workers 3 microservice.wsgi