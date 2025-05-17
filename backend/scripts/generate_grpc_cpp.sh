#!/bin/bash
set -euo pipefail

PROTO_DIR="/app/backend/protos/"
OUT_DIR="/app/backend/task_worker/generated/"
mkdir -p "$OUT_DIR"

# Generate
protoc \
  --experimental_allow_proto3_optional \
  -I="$PROTO_DIR" \
  --cpp_out="$OUT_DIR" \
  --grpc_out="$OUT_DIR" \
  --plugin=protoc-gen-grpc=$(which grpc_cpp_plugin) \
  "$PROTO_DIR/task_worker.proto"

# Verify output
ls -lah "$OUT_DIR/task_worker.grpc.pb.cc" "$OUT_DIR/task_worker.pb.cc"
