#include <iostream>
#include "systems/tortoise.hpp"

SysL::Tortoise::Tortoise() {}

void SysL::Tortoise::addRule(const std::string &expression) {
    auto delimiterIndex = (unsigned int) expression.find(RULE_EXPRESSION_DELIMITER);
    std::string ruleName = expression.substr(0, delimiterIndex);
    std::string ruleBody = expression.substr(delimiterIndex + 1, expression.size() - 1);
    rules.insert({ruleName, ruleBody});
}

void SysL::Tortoise::removeRule(const std::string &name) {
    rules.erase(name);
}

void SysL::Tortoise::clearRules() {
    rules.clear();
}

std::string SysL::Tortoise::generateAxiom(const std::string &expression, unsigned int iterations) {
    std::string result = expression;
    for (unsigned int i = 0; i < iterations; i++) {
        std::string newResult = result;
        for (auto it = rules.begin(); it != rules.end(); ++it) {
            std::string::size_type pos = 0;
            while ((pos = newResult.find(it->first, pos)) != std::string::npos) {
                newResult.replace(pos, it->first.length(), it->second);
                pos += it->second.length();
            }
        }
        result = std::move(newResult);
    }
    std::cout << "Processed result: " << result << std::endl;
    return result;
}