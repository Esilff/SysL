cmake_minimum_required(VERSION 3.12)
project(SysL VERSION 0.0.1 DESCRIPTION "A dynamic library to generate LSystem data representations" LANGUAGES CXX)

set(SYSL_TARGET_NAME ${PROJECT_NAME})
set(SYSL_INCLUDE_DIRS
        PUBLIC ${CMAKE_SOURCE_DIR}/include

)
set(SYSL_TARGET_SOURCES
        src/SysL.cpp

)



add_library(${SYSL_TARGET_NAME} ${SYSL_TARGET_SOURCES})

target_include_directories(${SYSL_TARGET_NAME} ${SYSL_INCLUDE_DIRS})
