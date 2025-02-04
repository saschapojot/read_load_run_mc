//
// Created by polya on 7/8/24.
//
#include "potentialFunctionPrototype.hpp"


class V2 : public potentialFunction {
public:
    V2(const std::string& funcName, const std::string &row) : potentialFunction() {
//        this->a1 = 1;
//        this->a2 = 1.5;
//        this-> c1 = 50;
//        this->c2 = 80;
        this->rowName = row;
        this->inParamsFile="./parameterFiles/"+funcName+"Params.txt";

        this->parseParams();




        this->paramStr = rowName;
        std::cout << "a1=" << a1 << ", a2=" << a2 << ", c1=" << c1 << ", c2=" << c2 << std::endl;


    }

public:
    std::string getParamStr() const override {
        return this->paramStr;
    }

public:
    double operator()(const double &L, const double &y0, const double &z0, const double &y1) const override {
        double val = c1 * std::pow(y0 - a1, 2) + c2 * std::pow(z0 - a2, 2)
                     + c1 * std::pow(y1 - a1, 2) + c2 * std::pow(-y0 - z0 - y1 + L - a2, 2);
//        std::cout<<"val="<<val<<std::endl;
        return val;

    }


    void parseParams() {

        std::regex rowRegex("(row\\d+)");
        std::regex a1Regex("a1\\s*=\\s*([+-]?(\\d+(\\.\\d*)?|\\.\\d+)([eE][+-]?\\d+)?)");
        std::regex a2Regex("a2\\s*=\\s*([+-]?(\\d+(\\.\\d*)?|\\.\\d+)([eE][+-]?\\d+)?)");
        std::regex c1Regex("c1\\s*=\\s*([+-]?(\\d+(\\.\\d*)?|\\.\\d+)([eE][+-]?\\d+)?)");
        std::regex c2Regex("c2\\s*=\\s*([+-]?(\\d+(\\.\\d*)?|\\.\\d+)([eE][+-]?\\d+)?)");

        std::smatch matchRow;
        std::smatch match_a1;
        std::smatch match_a2;
        std::smatch match_c1;
        std::smatch match_c2;

        std::ifstream file(inParamsFile);
        if (!file.is_open()) {
            std::cerr << "Error opening file: " << inParamsFile << std::endl;
            std::exit(1);
        }
        bool rowFound = false;
        std::string line;
        while (std::getline(file, line)) {
            // Process the line (e.g., print it)
//            std::cout << line << std::endl;
            //match row
            if (std::regex_search(line, matchRow, rowRegex)) {
                if (rowName == matchRow.str(1)) {
                    rowFound = true;
                }
                else{
                    continue;
                }

                //match params
                //match a1
                if (std::regex_search(line, match_a1, a1Regex)) {
                    this->a1 = std::stod(match_a1.str(1));
                } else {
                    std::cerr << "a1 missing." << std::endl;
                    std::exit(2);
                }

                //match a2
                if (std::regex_search(line, match_a2, a2Regex)) {
                    this->a2 = std::stod(match_a2.str(1));
                } else {
                    std::cerr << "a2 missing." << std::endl;
                    std::exit(2);
                }
                //match c1
                if (std::regex_search(line, match_c1, c1Regex)) {
                    this->c1 = std::stod(match_c1.str(1));
                } else {
                    std::cerr << "c1 missing." << std::endl;
                    std::exit(2);
                }

                //match c2
                if (std::regex_search(line, match_c2, c2Regex)) {
                    this->c2 = std::stod(match_c2.str(1));
                } else {
                    std::cerr << "c2 missing." << std::endl;
                    std::exit(2);
                }
            }


        }//end of while

        if (rowFound == false) {
            std::cerr << rowName + " not found." << std::endl;
            std::exit(3);
        }
    }// end of parseParams()




public:

    double a1;
    double a2;
    double c1;
    double c2;
    std::string paramStr;
    std::string rowName;
    std::string inParamsFile ;//= "./inputData/quadratic/quadraticCoeffs.txt";

};


class V24 : public potentialFunction {

public:
    V24(const std::string &funcName, const std::string &row) : potentialFunction() {
        this->rowName = row;
        this->inParamsFile = "./parameterFiles/" + funcName + "Params.txt";

        this->parseParams();
        this->paramStr = rowName;
        std::cout << "a1=" << a1 << ", a2=" << a2 << ", c12=" << c12 << ", c14=" << c14
        << ", c22="<<c22<<", c24="<<c24<<std::endl;

    }


public:
    std::string getParamStr() const override {
        return this->paramStr;
    }

    double operator()(const double &L, const double &y0, const double &z0, const double &y1) const override {
        double val = c12 * std::pow(y0 - a1, 2) + c14 * std::pow(y0 - a1, 4)
                     + c22 * std::pow(z0 - a2, 2) + c24 * std::pow(z0 - a2, 4) +
                     c12 * std::pow(y1 - a1, 2) + c14 * std::pow(y1 - a1, 4)
                     + c22 * std::pow(-y0 - z0 - y1 + L - a2, 2) + c24 * std::pow(-y0 - z0 - y1 + L - a2, 4);
        return val;
    }

    void parseParams() {
        std::regex rowRegex("(row\\d+)");
        std::regex a1Regex("a1\\s*=\\s*([+-]?(\\d+(\\.\\d*)?|\\.\\d+)([eE][+-]?\\d+)?)");
        std::regex a2Regex("a2\\s*=\\s*([+-]?(\\d+(\\.\\d*)?|\\.\\d+)([eE][+-]?\\d+)?)");
        std::regex c12Regex("c12\\s*=\\s*([+-]?(\\d+(\\.\\d*)?|\\.\\d+)([eE][+-]?\\d+)?)");

        std::regex c14Regex("c14\\s*=\\s*([+-]?(\\d+(\\.\\d*)?|\\.\\d+)([eE][+-]?\\d+)?)");
        std::regex c22Regex("c22\\s*=\\s*([+-]?(\\d+(\\.\\d*)?|\\.\\d+)([eE][+-]?\\d+)?)");
        std::regex c24Regex("c24\\s*=\\s*([+-]?(\\d+(\\.\\d*)?|\\.\\d+)([eE][+-]?\\d+)?)");

        std::smatch matchRow;
        std::smatch match_a1;
        std::smatch match_a2;
        std::smatch match_c12;
        std::smatch match_c14;
        std::smatch match_c22;
        std::smatch match_c24;
        std::ifstream file(inParamsFile);
        if (!file.is_open()) {
            std::cerr << "Error opening file: " << inParamsFile << std::endl;
            std::exit(1);
        }

        bool rowFound = false;
        std::string line;
        while (std::getline(file, line)) {
            if (std::regex_search(line, matchRow, rowRegex)) {

                if (rowName == matchRow.str(1)) {
                    rowFound = true;

                } else{
                    continue;
                }

                //match params
                //match a1
                if (std::regex_search(line, match_a1, a1Regex)) {
                    this->a1 = std::stod(match_a1.str(1));
                } else {
                    std::cerr << "a1 missing." << std::endl;
                    std::exit(2);
                }

                //match a2
                if (std::regex_search(line, match_a2, a2Regex)) {
                    this->a2 = std::stod(match_a2.str(1));
                } else {
                    std::cerr << "a2 missing." << std::endl;
                    std::exit(2);
                }

                //match c12
                if(std::regex_search(line,match_c12,c12Regex)){
                    this-> c12=std::stod(match_c12.str(1));
                }
                else {
                    std::cerr << "c12 missing." << std::endl;
                    std::exit(2);
                }
                //match c14
                if(std::regex_search(line,match_c14,c14Regex)){
                    this-> c14=std::stod(match_c14.str(1));
                }
                else {
                    std::cerr << "c14 missing." << std::endl;
                    std::exit(2);
                }
                //match c22
                if(std::regex_search(line,match_c22,c22Regex)){
                    this-> c22=std::stod(match_c22.str(1));
                }
                else {
                    std::cerr << "c22 missing." << std::endl;
                    std::exit(2);
                }

                //match c24
                if(std::regex_search(line,match_c24,c24Regex)){
                    this-> c24=std::stod(match_c24.str(1));
                }
                else {
                    std::cerr << "c24 missing." << std::endl;
                    std::exit(2);
                }


            }//end match row




        }//end while
        if (rowFound == false) {
            std::cerr << rowName + " not found." << std::endl;
            std::exit(3);
        }

    }//end of parseParams()

public:
    double c12;
    double c14;
    double c22;
    double c24;
    double a1;
    double a2;
    std::string paramStr;
    std::string rowName;
    std::string inParamsFile;


};

//factory function

std::shared_ptr<potentialFunction>  createPotentialFunction(const std::string& funcName, const std::string &row) {
    if (funcName == "V2") {

        return std::make_shared<V2>(funcName,row);
    } else if(funcName=="V24"){
        return std::make_shared<V24>(funcName,row);
    }

    else {
        throw std::invalid_argument("Unknown potential function type");
    }
}