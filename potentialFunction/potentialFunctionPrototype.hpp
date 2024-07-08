//
// Created by polya on 7/8/24.
//

#ifndef READ_LOAD_RUN_MC_POENTIALFUNCTIONPROTOTY_HPP
#define READ_LOAD_RUN_MC_POENTIALFUNCTIONPROTOTY_HPP
#include <fstream>
#include <iostream>
#include <math.h>
#include <memory>
#include <regex>
#include <stdexcept>
#include <string>

class potentialFunction {
//base class for potential function
public:
    virtual double operator()(const double&L,const double &y0, const double &z0, const double& y1) const = 0;
    virtual std::string getParamStr() const = 0; // Pure virtual function
    virtual ~ potentialFunction() {};
};






std::shared_ptr<potentialFunction>  createPotentialFunction(const std::string& funcName, const std::string &row) ;





#endif //READ_LOAD_RUN_MC_POENTIALFUNCTIONPROTOTY_HPP
