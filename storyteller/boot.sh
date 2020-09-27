#!/bin/sh

HOME="/src"

ls -lh /usr/bin/xray
/usr/bin/xray --bind=0.0.0.0:2000 --bind-tcp=0.0.0.0:2000 &

# Start gunicorn listening on all interfaces
exec gunicorn --chdir app storyteller:app \
              --workers 2 \
              --threads 4 \
              --access-logfile - \
              --error-logfile - \
              --timeout 300 \
              --bind 0.0.0.0:5000
