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
add_definitions(-DPYBIND11)
# This needs to be included before the pybind find_package to get the correct
# pyenv versions etc. Taken from
# https://github.com/pybind/pybind11/issues/99#issuecomment-531487569

execute_process(
  COMMAND which python
  OUTPUT_VARIABLE PYTHON_EXECUTABLE OUTPUT_STRIP_TRAILING_WHITESPACE
)

execute_process(
  COMMAND python -c "from __future__ import print_function; from distutils.sysconfig import get_python_inc; print(get_python_inc())"
  OUTPUT_VARIABLE PYTHON_INCLUDE_DIR OUTPUT_STRIP_TRAILING_WHITESPACE ERROR_QUIET
)

execute_process(
  COMMAND python -c "from __future__ import print_function; import os, numpy.distutils; print(os.pathsep.join(numpy.distutils.misc_util.get_numpy_include_dirs()))"
  OUTPUT_VARIABLE PYTHON_NUMPY_INCLUDE_DIR OUTPUT_STRIP_TRAILING_WHITESPACE ERROR_QUIET
)

execute_process(
  COMMAND python -c "from __future__ import print_function; import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR') + '/' + sysconfig.get_config_var('LDLIBRARY'))"
  OUTPUT_VARIABLE PYTHON_LIBRARY OUTPUT_STRIP_TRAILING_WHITESPACE ERROR_QUIET
)

execute_process(
  COMMAND python -c "from __future__ import print_function; import platform; print(platform.python_version())"
  OUTPUT_VARIABLE PYTHONLIBS_VERSION_STRING OUTPUT_STRIP_TRAILING_WHITESPACE ERROR_QUIET
)

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
