#!/usr/bin/env bash

celery -A config.celery worker --pool=threads --concurrency=4 --loglevel=info --without-gossip --without-mingle --without-heartbeat