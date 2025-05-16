#!/bin/bash
set -e

#grpc
/app/scripts/generate_grpc_python.sh

## Run migrations
alembic upgrade head

cd /app/web_app

# Start app // TODO: multiworker in prod
exec uvicorn app:app --host 0.0.0.0 --port 8000 --reload