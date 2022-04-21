cmake_minimum_required(VERSION 3.22)
if(NOT DEFINED CMAKE_TOOLCHAIN_FILE AND DEFINED ENV{CMAKE_TOOLCHAIN_FILE})
   set(CMAKE_TOOLCHAIN_FILE $ENV{CMAKE_TOOLCHAIN_FILE})
endif()
# name of the project It is best to use something different from the exe name
project(ThreadingBuilt) 

# Here we set the C++ standard to use
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(fmt CONFIG REQUIRED)
find_package(Threads CONFIG )

include_directories(../Logger/)

# grab all the cpp file names
file(GLOB SOURCE_FILES *.cpp)
# for each one generate a target the same name as the source file
foreach(SOURCE_PATH ${SOURCE_FILES})
    # remove the extension
    get_filename_component(EXECUTABLE_NAME ${SOURCE_PATH} NAME_WE)
    # create an exe and add link to pthread
    add_executable(${EXECUTABLE_NAME} ${SOURCE_PATH})
    target_link_libraries(${EXECUTABLE_NAME} PRIVATE  fmt::fmt-header-only pthread)

endforeach(SOURCE_PATH ${SOURCE_FILES})