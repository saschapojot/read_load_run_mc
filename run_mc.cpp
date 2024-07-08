#include "./mc_subroutine/mc_read_load_compute.hpp"
#include "./potentialFunction/poentialFunctionPrototype.hpp"

int main(int argc, char *argv[]) {

std::string funcName="V2";
std::string rowName="row0";

//auto potFuncPtr= createPotentialFunction(funcName,rowName);

std::string TStr="4";
std::string jsStr=R"({"L":1,"y0":2,"z0":3,"y1":4})";
std::string lp="1000000";
std::string fl="5";

std::string dataDir="./dataAll/"+funcName+"/"+rowName+"/T"+TStr+"/";
 std::string   U_dataFolder=dataDir+"/data_files/U_AllPickle/";
  std::string  dist_dataFolder=dataDir+"/data_files/dist_AllPickle/";

    auto mcObj=mc_computation(TStr,funcName,rowName,jsStr,lp,fl,"10",dataDir,U_dataFolder,dist_dataFolder);


}