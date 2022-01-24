cmake_minimum_required(VERSION 3.12)

if(NOT DEFINED CMAKE_TOOLCHAIN_FILE AND DEFINED ENV{CMAKE_TOOLCHAIN_FILE})
   set(CMAKE_TOOLCHAIN_FILE $ENV{CMAKE_TOOLCHAIN_FILE})
endif()

project(ExtendBuild)
# This is the name of the Exe change this and it will change everywhere
set(TargetName Extend)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

find_package (Python COMPONENTS Interpreter Development)



add_executable(${TargetName})

target_sources(${TargetName} PRIVATE ${PROJECT_SOURCE_DIR}/extend.cpp)
target_link_libraries(${TargetName} PRIVATE Python::Python)



