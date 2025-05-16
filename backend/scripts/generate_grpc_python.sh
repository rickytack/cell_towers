#!/bin/bash
OUT_DIR="/app/web_app/grpc_client/generated"

# Standard generation
python -m grpc_tools.protoc \
  -I/app/protos \
  --python_out="$OUT_DIR" \
  --grpc_python_out="$OUT_DIR" \
  /app/protos/task_worker.proto

# Force relative imports
sed -i 's/^import task_worker_pb2/from . import task_worker_pb2/' "$OUT_DIR"/*_grpc.py

# Set safe permissions (read-only)
chmod -R a+rX "$OUT_DIR"