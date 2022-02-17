cmake_minimum_required(VERSION 3.12)

if(NOT DEFINED CMAKE_TOOLCHAIN_FILE AND DEFINED ENV{CMAKE_TOOLCHAIN_FILE})
   set(CMAKE_TOOLCHAIN_FILE $ENV{CMAKE_TOOLCHAIN_FILE})
endif()

# Name of the project
project(TheComputerStoreBuild)
# This is the name of the Exe change this and it will change everywhere
set(TargetName TheComputerStore)
# use C++ 17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

find_path(SQLITE_MODERN_CPP_INCLUDE_DIRS "sqlite_modern_cpp.h")
# vcpkg not official sqltie support
find_package(unofficial-sqlite3 CONFIG REQUIRED)
 
add_executable(${TargetName})
target_sources(${TargetName} PRIVATE ${CMAKE_SOURCE_DIR}/store1.cpp)
target_include_directories(${TargetName} PRIVATE ${SQLITE_MODERN_CPP_INCLUDE_DIRS})
target_link_libraries(${TargetName} PRIVATE unofficial::sqlite3::sqlite3)



add_custom_target( MakeDB
    ALL 
    DEPENDS ${CMAKE_SOURCE_DIR}/createDatabase.sql
    COMMAND sqlite3  TheComputerStore.db < ${CMAKE_SOURCE_DIR}/createDatabase.sql
)


