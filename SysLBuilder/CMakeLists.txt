cmake_minimum_required(VERSION 3.5)
project(SysL VERSION 0.0.1 DESCRIPTION "A dynamic library to generate LSystem data representations" LANGUAGES CXX)

set(SYSL_TARGET_NAME ${PROJECT_NAME})

set(SYSL_TARGET_SOURCES
        src/SysL.cpp

        src/systems/tortoise.cpp
)

add_subdirectory(libs)

add_library(${SYSL_TARGET_NAME} SHARED ${SYSL_TARGET_SOURCES})


include(GenerateExportHeader)
generate_export_header(${SYSL_TARGET_NAME}
        BASE_NAME "SysL"
        EXPORT_MACRO_NAME "SYSL_API"
        EXPORT_FILE_NAME "export/SysL_export.hpp"
)

target_include_directories(${SYSL_TARGET_NAME}
        PUBLIC ${CMAKE_SOURCE_DIR}/include
        PUBLIC ${CMAKE_BINARY_DIR}/export
)

target_link_libraries(${SYSL_TARGET_NAME} PUBLIC glm)
