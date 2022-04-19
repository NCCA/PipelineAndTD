cmake_minimum_required(VERSION 3.12)
# Name of the project
project(QThreadBuild)
# This is the name of the Exe change this and it will change everywhere
set(TargetName QThread)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)

add_executable(${TargetName})

target_sources(${TargetName} PRIVATE  main.cpp MyThread.cpp MyThread.h)



target_link_libraries(${TargetName} PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)

