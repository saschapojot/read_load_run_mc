#include "./mc_subroutine/mc_read_load_compute.hpp"
#include "./potentialFunction/potentialFunctionPrototype.hpp"

int main(int argc, char *argv[]) {

//std::string funcName="V2";
//std::string rowName="row0";
//
////auto potFuncPtr= createPotentialFunction(funcName,rowName);
//
//std::string TStr="4";
//std::string jsStr=R"({"L":1,"y0":2,"z0":3,"y1":4})";
//std::string lp="1000000";
//std::string fl="5";
//
//std::string dataDir="./dataAll/"+funcName+"/"+rowName+"/T"+TStr+"/";
// std::string   U_dataFolder=dataDir+"/data_files/U_AllPickle/";
//  std::string  dist_dataFolder=dataDir+"/data_files/dist_AllPickle/";

//10 parameters are passed from *argv[]
    if (argc != 11) {
        std::cout << "wrong arguments" << std::endl;
        std::exit(2);
    }

    int paramIndStart=1;

    std::string TStr=std::string(argv[paramIndStart]);
    std::cout<<"TStr="<<TStr<<std::endl;

    std::string funcName=std::string(argv[paramIndStart+1]);
    std::cout<<"funcName="<<funcName<<std::endl;

    std::string rowName=std::string(argv[paramIndStart+2]);
    std::cout<<"rowName="<<rowName<<std::endl;

    std::string jsonInit=std::string(argv[paramIndStart+3]);
    std::cout<<"jsonInit="<<jsonInit<<std::endl;

    std::string loopToWriteStr=std::string(argv[paramIndStart+4]);
    std::cout<<"loopToWriteStr="<<loopToWriteStr<<std::endl;

    std::string newFlushNumStr=std::string(argv[paramIndStart+5]);
    std::cout<<"newFlushNumStr="<<newFlushNumStr<<std::endl;

    std::string loopLastFileStr=std::string(argv[paramIndStart+6]);
    std::cout<<"loopLastFileStr="<<loopLastFileStr<<std::endl;

    std::string dataDir=std::string (argv[paramIndStart+7]);
    std::cout<<"dataDir="<<dataDir<<std::endl;

    std::string U_Dir=std::string(argv[paramIndStart+8]);
    std::cout<<"U_Dir="<<U_Dir<<std::endl;

    std::string dist_Dir=std::string (argv[paramIndStart+9]);
    std::cout<<"dist_Dir="<<dist_Dir<<std::endl;







    auto mcObj=mc_computation(TStr,funcName,rowName,
                              jsonInit,loopToWriteStr,newFlushNumStr,
                              loopLastFileStr,dataDir,U_Dir,dist_Dir);
    mcObj.init_and_run();


}