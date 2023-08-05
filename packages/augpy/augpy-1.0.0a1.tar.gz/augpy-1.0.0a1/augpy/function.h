#ifndef AUGPY_FUNCTIONS_H
#define AUGPY_FUNCTIONS_H


#include <string>
#include <utility>
#include <cuda.h>
#include <pybind11/pybind11.h>
#include "nvToolsExt.h"


namespace augpy {


void init();


std::tuple<size_t, size_t, size_t> meminfo(int device_id);


void enable_profiler();


void disable_profiler();


nvtxRangeId_t nvtx_range_start(std::string msg);


void nvtx_range_end(nvtxRangeId_t end);


// namespace augpy
}


// AUGPY_FUNCTIONS_H
#endif
