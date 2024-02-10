#include <iostream>
#include "SysL.hpp"
#include "systems/tortoise.hpp"

void* getTortoiseSystem() {
    auto * system = new SysL::Tortoise();
    return static_cast<void*>(system);
}

void addRule(void* system, const char* expression) {
    auto * castSystem = static_cast<SysL::Tortoise*>(system);
    castSystem->addRule(expression);
}

void removeRule(void* system, const char* name) {
    auto * castSystem = static_cast<SysL::Tortoise*>(system);
    castSystem->removeRule(name);
}

void clearRules(void* system) {
    auto * castSystem = static_cast<SysL::Tortoise*>(system);
    castSystem->clearRules();
}

const char* generateAxiom(void* system, const char* axiom, unsigned int iterations) {
    auto * castSystem = static_cast<SysL::Tortoise*>(system);
    static std::string result = castSystem->generateAxiom(axiom, iterations);
    std::cout << "Final result : " << castSystem->generateAxiom(axiom, iterations) << std::endl;
    return result.c_str();
}
