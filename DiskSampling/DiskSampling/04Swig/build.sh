#!/bin/bash

swig -python -py3 -c++ -I../../common ../src/PoissonDisk.i
clang++ -std=c++17 -Wall -g -c `python-config --cflags` ../../common/*.cpp ../src/*.cxx -I../../common
clang++ --shared -std=c++17 -g -L/opt/homebrew/lib `python-config --ldflags --libs --embed`  *.o -o PoissonDisk.so