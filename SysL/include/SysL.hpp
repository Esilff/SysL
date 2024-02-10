#ifndef __SYSL_HPP__
#define __SYSL_HPP__

#include <SysL_export.hpp>

extern "C" {
    SYSL_API void* getTortoiseSystem();

    SYSL_API void addRule(void* system, const char* expression);
    SYSL_API void removeRule(void* system, const char* name);
    SYSL_API void clearRules(void* system);
    SYSL_API const char* generateAxiom(void* system, const char* axiom, unsigned int iterations);
};

#endif