cmake_minimum_required(VERSION 3.20)
project(goe_fast_features LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
add_library(goe_fast_features SHARED rolling_features.cpp)
