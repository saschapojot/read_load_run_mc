//
// Created by polya on 7/8/24.
//

#ifndef READ_LOAD_RUN_MC_MC_READ_LOAD_COMPUTE_HPP
#define READ_LOAD_RUN_MC_MC_READ_LOAD_COMPUTE_HPP
#include "../potentialFunction/potentialFunctionPrototype.hpp"



#include <boost/filesystem.hpp>
#include <boost/python.hpp>
#include <boost/python/object/pickle_support.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include <chrono>
#include <cstdlib>
#include <cxxabi.h>
#include <fstream>
#include <initializer_list>
#include <iomanip>
#include <iostream>
#include <math.h>
#include <memory>
#include <random>
#include <regex>
#include <sstream>
#include <string>
#include <typeinfo>
#include <vector>
namespace fs = boost::filesystem;



class mc_computation {
public:
    mc_computation(const std::string &TStr, const std::string &funcName, const std::string &rowName,
                   const std::string &jsonData,
                   const std::string &loopToWriteStr, const std::string &newFlushNumStr, const std::string &loopLastFileStr,
                  const std::string &dataDirStr, const std::string& U_DirStr, const std::string &dist_DirStr) {


        //parse T
        try {
            this->T = std::stod(TStr); // Attempt to convert string to double

        } catch (const std::invalid_argument &e) {
            std::cerr << "Invalid argument: " << e.what() << std::endl;
            std::exit(1);
        } catch (const std::out_of_range &e) {
            std::cerr << "Out of range: " << e.what() << std::endl;
            std::exit(1);
        }

        if (T <= 0) {
            std::cerr << "T must be >0" << std::endl;
            std::exit(1);
        }
        this->beta = 1 / T;
        double stepForT1 = 0.1;
        this->h = stepForT1 * T > 0.2 ? 0.2 : stepForT1 * T;//stepSize;
        std::cout << "h=" << h << std::endl;



        //set potential function
        this->potFuncPtr = createPotentialFunction(funcName, rowName);

        //parse json to get initial value
        this->parseJsonData(jsonData, this->LInit, this->y0Init, this->z0Init, this->y1Init);
        this->varNum = 4;
        //parse loopToWrite

        try {
            this->loopToWrite = std::stoull(loopToWriteStr);
        }
        catch (const std::invalid_argument &e) {
            std::cerr << "Invalid argument: " << e.what() << std::endl;
            std::exit(1);
        } catch (const std::out_of_range &e) {
            std::cerr << "Out of range: " << e.what() << std::endl;
            std::exit(1);
        }

        //parse new flush number

        try {
            this->newFlushNum = std::stoull(newFlushNumStr);
        }
        catch (const std::invalid_argument &e) {
            std::cerr << "Invalid argument: " << e.what() << std::endl;
            std::exit(1);
        } catch (const std::out_of_range &e) {
            std::cerr << "Out of range: " << e.what() << std::endl;
            std::exit(1);
        }

        //parse loop in last file
        try{
            this->loopLastFile=std::stoull(loopLastFileStr);
        }
        catch (const std::invalid_argument &e) {
            std::cerr << "Invalid argument: " << e.what() << std::endl;
            std::exit(1);
        } catch (const std::out_of_range &e) {
            std::cerr << "Out of range: " << e.what() << std::endl;
            std::exit(1);
        }


        this->dataDir=dataDirStr;
        this->U_dataFolder=U_DirStr;
        this->dist_dataFolder=dist_DirStr;


        //allocate arrays
        try {
            U_ptr = std::shared_ptr<double[]>(new double[loopToWrite],
                                              std::default_delete<double[]>());
            dist_ptr = std::shared_ptr<double[]>(new double[loopToWrite * varNum],
                                                 std::default_delete<double[]>());
        }
        catch (const std::bad_alloc &e) {
            std::cerr << "Memory allocation error: " << e.what() << std::endl;
        } catch (const std::exception &e) {
            std::cerr << "Exception: " << e.what() << std::endl;
        }

//    std::cout<<"T="<<T<<", beta="<<beta
//    <<", LInit="<<LInit<<", y0Init="<<y0Init
//    <<", z0Init="<<z0Init<<", y1Init="<<y1Init
//    <<", loopToWrite="<<loopToWrite<<", newFlushNum="<<newFlushNumStr<<std::endl;


    }

public:
    ///
    /// @param jsonDataStr json data containing initial values of distances
    /// @param LInit
    /// @param y0Init
    /// @param z0Init
    /// @param y1Init
    void parseJsonData(const std::string &jsonDataStr, double &LInit, double &y0Init, double &z0Init, double &y1Init);

    void execute_mc(const double& L,const double &y0, const double &z0, const double& y1, const size_t & loopInit, const size_t & flushNum);
    ///
    /// @param LCurr current value of L
    /// @param y0Curr current value of y0
    /// @param z0Curr current value of z0
    /// @param y1Curr current value of y1
    /// @param LNext  next value of L
    /// @param y0Next next value of y0
    /// @param z0Next next value of z0
    /// @param y1Next next value of y1
    void proposal(const double &LCurr, const double& y0Curr,const double& z0Curr, const double& y1Curr,
                  double & LNext, double & y0Next, double & z0Next, double & y1Next);

    ///
    /// @param x
    /// @param sigma
    /// @return a value around x, from a  normal distribution
    static double generate_nearby_normal(const double & x, const double &sigma){
        std::random_device rd;  // Random number generator
        std::mt19937 gen(rd()); // Mersenne Twister engine
        std::normal_distribution<> d(x, sigma); // Normal distribution with mean rCurr and standard deviation sigma

        double xNext = d(gen);


        return xNext;


    }
    ///
    /// @param LCurr
    /// @param y0Curr
    /// @param z0Curr
    /// @param y1Curr
    /// @param LNext
    /// @param y0Next
    /// @param z0Next
    /// @param y1Next
    /// @param UNext
    /// @return
    double acceptanceRatio(const double &LCurr,const double &y0Curr,
                           const double &z0Curr, const double& y1Curr,const double& UCurr,
                           const double &LNext, const double& y0Next,
                           const double & z0Next, const double & y1Next,
                           double &UNext);
    void init_and_run();

    //read and write to pickle
    static void save_array_to_pickle(std::shared_ptr<double[]> &ptr, std::size_t size, const std::string& filename) {
        using namespace boost::python;
        try {
            Py_Initialize();  // Initialize the Python interpreter
            if (!Py_IsInitialized()) {
                throw std::runtime_error("Failed to initialize Python interpreter");
            }

            // Debug output
            std::cout << "Python interpreter initialized successfully." << std::endl;

            // Import the pickle module
            object pickle = import("pickle");
            object pickle_dumps = pickle.attr("dumps");

            // Create a Python list from the C++ array
            list py_list;
            for (std::size_t i = 0; i < size; ++i) {
                py_list.append(ptr[i]);
            }

            // Serialize the list using pickle.dumps
            object serialized_array = pickle_dumps(py_list, 2);  // Use protocol 2 for binary compatibility

            // Extract the serialized data as a string
            std::string serialized_str = extract<std::string>(serialized_array);

            // Write the serialized data to a file
            std::ofstream file(filename, std::ios::binary);
            if (!file) {
                throw std::runtime_error("Failed to open file for writing: " + filename);
            }
            file.write(serialized_str.data(), serialized_str.size());
            file.close();

            // Debug output
            std::cout << "Array serialized and written to file successfully." << std::endl;
        } catch (const error_already_set&) {
            PyErr_Print();
            std::cerr << "Boost.Python error occurred while saving array to pickle file." << std::endl;
        } catch (const std::exception& e) {
            std::cerr << "Exception: " << e.what() << std::endl;
        }

        if (Py_IsInitialized()) {
            Py_Finalize();  // Finalize the Python interpreter
        }
    }

public:
    double T;// temperature
    double beta;
    double h;// step size
    size_t loopToWrite;
    size_t newFlushNum;
    size_t loopLastFile;
    std::shared_ptr<potentialFunction> potFuncPtr;
    std::string dataDir;
    std::string U_dataFolder;
    std::string dist_dataFolder;
    std::string summary_folder;
    std::string data_root;
    std::string TFolder;
    std::shared_ptr<double[]> U_ptr;
    std::shared_ptr<double[]> dist_ptr;

    size_t varNum;

    double LInit;
    double y0Init;
    double z0Init;
    double y1Init;
};







#endif //READ_LOAD_RUN_MC_MC_READ_LOAD_COMPUTE_HPP
