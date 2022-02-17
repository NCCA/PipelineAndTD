cmake_minimum_required(VERSION 3.12)

if(NOT DEFINED CMAKE_TOOLCHAIN_FILE AND DEFINED ENV{CMAKE_TOOLCHAIN_FILE})
   set(CMAKE_TOOLCHAIN_FILE $ENV{CMAKE_TOOLCHAIN_FILE})
endif()

# Name of the project
project(CheckScores)
# This is the name of the Exe change this and it will change everywhere
# use C++ 17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)
# vcpkg not official sqltie support
find_package(unofficial-sqlite3 CONFIG REQUIRED)
 
set(TargetName CheckScores)
add_executable(${TargetName})
target_sources(${TargetName} PRIVATE ${CMAKE_SOURCE_DIR}/checkScores.cpp)
target_link_libraries(${TargetName} PRIVATE unofficial::sqlite3::sqlite3)

add_custom_target( MakeDB
    ALL 
    DEPENDS ${CMAKE_SOURCE_DIR}/createDatabase.sql
    COMMAND sqlite3  scores.db < ${CMAKE_SOURCE_DIR}/createDatabase.sql
)

add_custom_target(${TargetName}CopyPython ALL
COMMAND ${CMAKE_COMMAND} -E copy
    ${CMAKE_CURRENT_SOURCE_DIR}/checkScores.py
    ${CMAKE_CURRENT_BINARY_DIR}/checkScores.py
)
