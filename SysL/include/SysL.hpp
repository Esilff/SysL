#ifndef __SYSL_HPP__
#define __SYSL_HPP__

#include <SysL_export.hpp>

extern "C" {
    void* getEnvironment();
    const char* processAxiom(const char* axiom, unsigned int iterations, float alpha);
};

#endif