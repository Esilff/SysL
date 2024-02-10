#ifndef __SYSL_TORTOISE_HPP__
#define __SYSL_TORTOISE_HPP__
#include <stack>
#include <array>
#include <string>
#include <map>
#include <glm/glm.hpp>

#define RULE_EXPRESSION_DELIMITER '='


namespace SysL {

    class Tortoise {
    public:
        Tortoise();

    public:

        std::string SysL::Tortoise::generateAxiom(const std::string &expression, unsigned int iterations);


        void addRule(const std::string& expression);
        void removeRule(const std::string& name);
        void clearRules();

    private:


        std::map<const std::string, const std::string> rules;
        std::stack<glm::vec3> positionStack;

        std::array<char, 9> operators {'+','-','&', '^', '<', '>', '|', '[', ']'};



    };

}

#endif