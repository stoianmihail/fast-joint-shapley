cmake_minimum_required(VERSION 3.22)

project (joint-shapley)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native -O3")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g -Wall -Wextra")

find_package(Threads REQUIRED)
set(THREADS_PREFER_PTHREAD_FLAG ON)

# Build the shared library.
add_library(joint-shapley SHARED joint_shapley.cc)
