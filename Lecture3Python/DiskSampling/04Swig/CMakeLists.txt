cmake_minimum_required(VERSION 3.12)

if(NOT DEFINED CMAKE_TOOLCHAIN_FILE AND DEFINED ENV{CMAKE_TOOLCHAIN_FILE})
   set(CMAKE_TOOLCHAIN_FILE $ENV{CMAKE_TOOLCHAIN_FILE})
endif()

project(PoissonSWIGModuleBuild)
# This is the name of the Exe change this and it will change everywhere
set(TargetName PoissonDisk)
find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

# Set to C++ 17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)
option(ENABLE_FAST_MATH ON)

find_package (Python3 COMPONENTS  Development)

message("found python " ${Python_EXECUTABLE})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../common)

set(CMAKE_SWIG_FLAGS "-builtin")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
link_directories(/opt/homebrew/lib)
set_source_files_properties(${CMAKE_CURRENT_SOURCE_DIR}/src/PoissonDisk.i PROPERTIES CPLUSPLUS ON)
#set_source_files_properties(${CMAKE_CURRENT_SOURCE_DIR}/src/PoissonDisk.i PROPERTIES SWIG_FLAGS "-includeall")

swig_add_library(${TargetName}  TYPE MODULE LANGUAGE python SOURCES 
${CMAKE_CURRENT_SOURCE_DIR}/src/PoissonDisk.i
${CMAKE_CURRENT_SOURCE_DIR}/../common/PoissonDisk.cpp
)
swig_link_libraries(${TargetName} Python3::Python )

