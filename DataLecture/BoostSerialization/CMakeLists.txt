cmake_minimum_required(VERSION 3.12)

if(NOT DEFINED CMAKE_TOOLCHAIN_FILE AND DEFINED ENV{CMAKE_TOOLCHAIN_FILE})
    set(CMAKE_TOOLCHAIN_FILE $ENV{CMAKE_TOOLCHAIN_FILE})
endif()

project(BootSerialization VERSION 1.0 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)


include_directories(include)

find_package(Boost REQUIRED COMPONENTS serialization)


add_executable(Sphere src/main.cpp src/Sphere.cpp include/Sphere.h)
target_link_libraries(Sphere PRIVATE Boost::serialization)
