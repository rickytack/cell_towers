FROM ubuntu:22.04 AS builder

# Install build dependencies
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

# Verify the CMakeLists.txt location
RUN ls -la /app/backend/task_worker/

# Generate from proto
RUN bash /app/backend/scripts/generate_grpc_cpp.sh

# Build
RUN mkdir -p /app/build && \
    cd /app/build && \
    cmake ../backend/task_worker -DCMAKE_BUILD_TYPE=Release && \
    cmake --build . -- -j$(nproc)


FROM ubuntu:22.04

# Runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libprotobuf23 \
    libgrpc++1 \
    libcgal-dev # TODO: replace with non dev package

COPY --from=builder /app/build/task_worker /usr/local/bin/


CMD ["task_worker"]
