#!/bin/bash
set -e

#grpc
/app/scripts/generate_grpc_python.sh

## Run migrations
alembic upgrade head

cd /app/web_app

# Start app
if [ "$1" = "dev" ]; then
    echo "Running in development mode"
    exec uvicorn app:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Running in production mode"
    # Calculate optimal worker count
    WORKERS=$((2 * $(nproc --all) + 1))
    echo "Starting gunicorn with $WORKERS workers"
    exec gunicorn \
        -w "$WORKERS" \
        -k "uvicorn.workers.UvicornWorker" \
        --bind "0.0.0.0:8000" \
        --timeout 120 \
        --keep-alive 5 \
        --access-logfile - \
        app:app
fi