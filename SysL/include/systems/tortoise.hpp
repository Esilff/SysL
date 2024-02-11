#ifndef __SYSL_TORTOISE_HPP__
#define __SYSL_TORTOISE_HPP__
#include <stack>
#include <array>
#include <vector>
#include <string>
#include <map>
#include <glm/glm.hpp>


#define RULE_EXPRESSION_DELIMITER '='


namespace SysL {

    struct SystemData {
        std::vector<float> vertices;
        std::vector<int> indices;
    };

    class Tortoise {
    public:
        Tortoise();

    public:

        std::string generateAxiom(const std::string &expression, unsigned int iterations);
        void computeAxiom(const std::string& axiom, glm::vec3 origin, float alpha);




        void addRule(const std::string& expression);
        void removeRule(const std::string& name);
        void clearRules();

    private:


        std::map<const std::string, const std::string> rules;

        std::vector<glm::vec3> positions;
        std::stack<glm::vec3> positionStack;
        SystemData data;

        std::array<char, 9> operators {'+','-','&', '^', '<', '>', '|', '[', ']'};

        void generateTrunk(glm::vec3 point, float radius, unsigned int segments);



    };

}

#endif