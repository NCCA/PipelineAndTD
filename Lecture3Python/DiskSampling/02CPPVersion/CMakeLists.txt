cmake_minimum_required(VERSION 3.12)

if(NOT DEFINED CMAKE_TOOLCHAIN_FILE AND DEFINED ENV{CMAKE_TOOLCHAIN_FILE})
   set(CMAKE_TOOLCHAIN_FILE $ENV{CMAKE_TOOLCHAIN_FILE})
endif()

project(PoissonBuild)
# This is the name of the Exe change this and it will change everywhere
set(TargetName Poisson)
# Set to C++ 17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)
option(ENABLE_FAST_MATH ON)

add_executable(${TargetName})
target_include_directories(${TargetName} PRIVATE ${PROJECT_SOURCE_DIR}/include)
target_include_directories(${TargetName} PRIVATE ${PROJECT_SOURCE_DIR}/../common)

target_sources(${TargetName} PRIVATE ${PROJECT_SOURCE_DIR}/src/main.cpp
${PROJECT_SOURCE_DIR}/../common/PoissonDisk.cpp
${PROJECT_SOURCE_DIR}/../common/PoissonDisk.h
)




