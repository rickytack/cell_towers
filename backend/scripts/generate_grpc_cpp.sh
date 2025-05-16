#!/bin/bash
set -euo pipefail

# Directory setup
PROTO_DIR="/home/solomin/PET/Cells/cell-tower/backend/protos/"
OUT_DIR="/home/solomin/PET/Cells/cell-tower/backend/task_worker/generated/"
mkdir -p "$OUT_DIR"

# Generate protobuf and gRPC code
protoc \
  -I="$PROTO_DIR" \
  --cpp_out="$OUT_DIR" \
  --grpc_out="$OUT_DIR" \
  --plugin=protoc-gen-grpc=$(which grpc_cpp_plugin) \
  "$PROTO_DIR/task_worker.proto"

# Verify output
ls -lah "$OUT_DIR/task_worker.grpc.pb.cc" "$OUT_DIR/task_worker.pb.cc"