cmake_minimum_required(VERSION 3.27)
project(read_load_run_mc)

set(CMAKE_CXX_STANDARD 17)

include_directories(mc_subroutine)
include_directories(potentialFunction)

add_executable(run_mc
        mc_subroutine/mc_read_load_compute.cpp
        potentialFunction/potentialFunctions.cpp
        run_mc.cpp)


set(Python3_INCLUDE_DIRS "/home/polya/anaconda3/include/python3.9")
set(Python3_LIBRARIES "/home/polya/anaconda3/lib/libpython3.9.so.1.0")
include_directories(${Python3_INCLUDE_DIRS})

set_source_files_properties(
        mc_subroutine/mc_read_load_compute.cpp
        PROPERTIES

        COMPILE_OPTIONS "-O3"
)

set_source_files_properties(
        potentialFunction/potentialFunctions.cpp
        PROPERTIES

        COMPILE_OPTIONS "-O3"
)

set(Boost_NO_SYSTEM_PATHS YES)
if (Boost_NO_SYSTEM_PATHS)
    set(Boost_ROOT "/home/polya/cppLocal/boostBuild")
    set(Boost_INCLUDE_DIR "/home/polya/cppLocal/boostBuild/include")
    set(Boost_LIBRARY_DIR "/home/polya/cppLocal/boostBuild/lib")
endif (Boost_NO_SYSTEM_PATHS)


find_package(Boost  REQUIRED filesystem json python${Python3_VERSION_MAJOR}${Python3_VERSION_MINOR})
if(Boost_FOUND)
    message(STATUS "boost root is: ${Boost_ROOT}")
    message(STATUS "boost include path is : ${Boost_INCLUDE_DIR}")
    message(STATUS "boost library path is : ${Boost_LIBRARY_DIR}")
    message(STATUS "boost libraries is : ${Boost_LIBRARIES}")
    include_directories(${Boost_INCLUDE_DIR})
    link_directories(${Boost_LIBRARY_DIR})
else()
    message(WARNING "boost not found.")
endif()

target_link_libraries(run_mc Boost::filesystem)
target_link_libraries(run_mc Boost::python)
target_link_libraries(run_mc ${Python3_LIBRARIES})
target_link_libraries(run_mc Boost::json)