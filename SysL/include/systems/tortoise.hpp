#ifndef __SYSL_TORTOISE_HPP__
#define __SYSL_TORTOISE_HPP__
#include <stack>
#include <string>
#include <map>

namespace SysL {

    class Tortoise {
    public:
        Tortoise();
    private:
        std::map<const std::string, const std::string> rules;

    };

}

#endif