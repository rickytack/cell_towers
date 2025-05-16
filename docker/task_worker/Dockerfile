# Dockerfile for C++ task worker built with CMake (Ubuntu 22.04 LTS)
FROM ubuntu:22.04 AS builder

# Install build dependencies with pinned versions
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    pkg-config \
    protobuf-compiler \
    libprotobuf-dev \
    libgrpc++-dev \
    libgrpc-dev \
    protobuf-compiler-grpc \
    libcgal-dev

WORKDIR /app
COPY . .

# Verify the CMakeLists.txt location (debug)
RUN ls -la /app/backend/task_worker/

# Build with correct paths
RUN mkdir -p /app/build && \
    cd /app/build && \
    cmake ../backend/task_worker -DCMAKE_BUILD_TYPE=Release && \
    cmake --build . -- -j$(nproc)

# Minimal runtime image
FROM ubuntu:22.04

# Runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libprotobuf23 \
    libgrpc++1 \
    libcgal-dev

# Copy the binary
COPY --from=builder /app/build/task_worker /usr/local/bin/


CMD ["task_worker"]
