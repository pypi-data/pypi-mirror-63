#include <cuda_profiler_api.h>
#include "function.h"
#include "exception.h"


void augpy::init() {
    CUDA(cudaSetDevice(0));
    CUDA(cudaSetDeviceFlags(cudaDeviceScheduleYield));
}


std::tuple<size_t, size_t, size_t> augpy::meminfo(int device_id) {
    size_t free;
    size_t total;
    CUDA(cudaSetDevice(device_id));
    CUDA(cudaMemGetInfo(&free, &total));
    return std::make_tuple(total - free, free, total);
}


void augpy::enable_profiler() {
    CUDA(cudaProfilerStart());
}


void augpy::disable_profiler() {
    CUDA(cudaProfilerStop());
}


nvtxRangeId_t augpy::nvtx_range_start(std::string msg) {
    return nvtxRangeStartA(msg.c_str());
}


void augpy::nvtx_range_end(nvtxRangeId_t end) {
    nvtxRangeEnd(end);
}
