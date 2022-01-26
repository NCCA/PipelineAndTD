cmake_minimum_required(VERSION 3.12)

if(NOT DEFINED CMAKE_TOOLCHAIN_FILE AND DEFINED ENV{CMAKE_TOOLCHAIN_FILE})
   set(CMAKE_TOOLCHAIN_FILE $ENV{CMAKE_TOOLCHAIN_FILE})
endif()

project(PoissonModuleBuild)
# This is the name of the Exe change this and it will change everywhere
set(TargetName PoissonDisk)
# Set to C++ 17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)
option(ENABLE_FAST_MATH ON)

find_package(pybind11 CONFIG REQUIRED)
pybind11_add_module(${TargetName} NO_EXTRAS)

target_include_directories(${TargetName} PRIVATE ${PROJECT_SOURCE_DIR}/../common)
target_sources(${TargetName} PRIVATE 

${PROJECT_SOURCE_DIR}/src/PythonBindings.cpp
${PROJECT_SOURCE_DIR}/../common/PoissonDisk.cpp
${PROJECT_SOURCE_DIR}/../common/PoissonDisk.h

)

target_link_libraries(${TargetName} PRIVATE   pybind11::module)

add_custom_target(${TargetName}CopyPython ALL
	COMMAND ${CMAKE_COMMAND} -E copy
    ${CMAKE_CURRENT_SOURCE_DIR}/test.py
    ${CMAKE_CURRENT_BINARY_DIR}/test.py

) 
