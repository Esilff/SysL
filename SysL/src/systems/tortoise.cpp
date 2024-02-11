#include <iostream>
#include "systems/tortoise.hpp"
#include "glm/ext/matrix_transform.hpp"

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

void SysL::Tortoise::computeAxiom(const std::string &axiom, glm::vec3 origin, float alpha) {
    positions.push_back(origin);
    glm::vec3 nextPosition = origin;
    glm::vec4 nextVector = glm::vec4(0.0,0.0,1.0,0.0);
    float radians = glm::radians(alpha);
    for (auto character : axiom) {
        switch(character){
            case 'F':
                nextPosition += glm::vec3(nextVector);
                positions.push_back(nextPosition);
                break;
            case '+':
                nextVector = glm::rotate(glm::mat4(1.0f), radians, glm::vec3(0.0f,0.0f,1.0f)) * nextVector;
                break;
            case '-':
                nextVector = glm::rotate(glm::mat4(1.0f), -radians, glm::vec3(0.0f,0.0f,1.0f)) * nextVector;
                break;
            case '&':
                nextVector = glm::rotate(glm::mat4(1.0f), -radians, glm::vec3(0.0f,1.0f,0.0f)) * nextVector;
                break;
            case '^':
                nextVector = glm::rotate(glm::mat4(1.0f), radians, glm::vec3(0.0f,1.0f,0.0f)) * nextVector;
                break;
            case '<':
                nextVector = glm::rotate(glm::mat4(1.0f), -radians, glm::vec3(1.0f,0.0f,0.0f)) * nextVector;
                break;
            case '>':
                nextVector = glm::rotate(glm::mat4(1.0f), radians, glm::vec3(1.0f,0.0f,0.0f)) * nextVector;
                break;
            case '|':
                break;
            case '[':
                positionStack.push(nextPosition);
                break;
            case ']':
                nextPosition = positionStack.top();
                positionStack.pop();
                break;
        }
    }
}

void SysL::Tortoise::generateTrunk(glm::vec3 point, float radius, unsigned int segments) {
    for (int i = 0; i < segments; i++) {
        double angle = (2.0 * M_PI) / segments * i;
        double dx = radius * cos( angle);
        double dy = radius * sin(angle);
        data.vertices.push_back(point.x + (float) dx);
        data.vertices.push_back(point.y + (float) dy);
        data.vertices.push_back(point.z);
    }
    if (data.vertices.size() <= segments) {
        auto size = data.vertices.size();
        for (auto i = size - 6; i < size; i++) {
            data.indices.push_back((int)i + 1 > size ? (int) i : (int)i + 1);
            data.indices.push_back((int)i);
            data.indices.push_back((int)i - 6);
            data.indices.push_back((int)i - 5);
        }
    }
}