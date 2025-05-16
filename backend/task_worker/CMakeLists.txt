cmake_minimum_required(VERSION 3.13)

set(MODULE_NAME "task_worker")
project(${MODULE_NAME} VERSION 1.0.0 DESCRIPTION "Task worker")
add_definitions(-DPROJECT_VERSION="${${MODULE_NAME}_VERSION}")
add_definitions(-DDESCRIPTION="${${MODULE_NAME}_DESCRIPTION}")

set(CMAKE_CXX_STANDARD 20)

### SOURCE CODE
file(GLOB SRC_FILES
        src/task_worker_service.h
        src/task_worker_service.cpp
)

file(GLOB PROTO_SRCS "${CMAKE_CURRENT_SOURCE_DIR}/generated/*.cc")

### DEPENDENCIES
find_package(Protobuf REQUIRED)

# Protobuf
set(LIBS ${LIBS}
        protobuf::libprotobuf
        grpc++
        #grpc++_reflection
)

# CGA
find_package(CGAL REQUIRED)
set(LIBS ${LIBS} CGAL::CGAL)

### LINKING
add_executable(${MODULE_NAME}
        src/main.cpp
        ${SRC_FILES}
        ${PROTO_SRCS}
)


target_include_directories(${MODULE_NAME} PRIVATE ${GENERATED_DIR})
target_link_libraries(${MODULE_NAME} PRIVATE ${LIBS})