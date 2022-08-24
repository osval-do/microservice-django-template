#!/usr/bin/env sh

# Collect static files
python manage.py collectstatic --noinput

# Apply any pending database migration
python manage.py migrate

# Uncomment to use cron service in microservice backend
# env > /opt/evars.sh
# service cron start >> logs/cron.log 2>&1

# Start server
daphne -b 0.0.0.0 -p 8000 microservice.asgi:application