#!/usr/bin/env bash
set -e

: "${DJANGO_SETTINGS_MODULE:=config.settings}"
: "${DJANGO_WSGI_MODULE:=config.wsgi:application}"
: "${GUNICORN_BIND:=0.0.0.0:8080}"
: "${GUNICORN_WORKERS:=3}"
: "${GUNICORN_TIMEOUT:=60}"

export DJANGO_SETTINGS_MODULE

gunicorn "$DJANGO_WSGI_MODULE" \
  --bind "$GUNICORN_BIND" \
  --workers "$GUNICORN_WORKERS" \
  --timeout "$GUNICORN_TIMEOUT" \
  --access-logfile - \
  --error-logfile -