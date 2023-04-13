cmake_minimum_required(VERSION 3.12)

if(NOT DEFINED CMAKE_TOOLCHAIN_FILE AND DEFINED ENV{CMAKE_TOOLCHAIN_FILE})
    set(CMAKE_TOOLCHAIN_FILE $ENV{CMAKE_TOOLCHAIN_FILE})
endif()

project(AllProtoBuf VERSION 1.0 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)


find_package(protobuf CONFIG REQUIRED)

include_directories(${Protobuf_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_BINARY_DIR})

set(PROTO_FILES scene.proto)
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${PROTO_FILES})
protobuf_generate_python(PROTO_PY ${PROTO_FILES})

add_executable(write write.cpp ${PROTO_SRCS} ${PROTO_HDRS})
target_link_libraries(write PRIVATE protobuf::libprotoc protobuf::libprotobuf protobuf::libprotobuf-lite)


add_executable(read read.cpp ${PROTO_SRCS} ${PROTO_HDRS})
target_link_libraries(read PRIVATE protobuf::libprotoc protobuf::libprotobuf protobuf::libprotobuf-lite)

add_custom_target(PythonBuild ALL DEPENDS read.py)
