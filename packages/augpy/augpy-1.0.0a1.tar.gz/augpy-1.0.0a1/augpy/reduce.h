#ifndef AUGPY_REDUCE_H
#define AUGPY_REDUCE_H


#include <curand.h>
#include <curand_kernel.h>
#include "tensor.h"


namespace augpy {


CudaTensor* sum(
    CudaTensor* tensor,
    bool upcast
);


CudaTensor* sum_axis(
    CudaTensor* tensor,
    int axis,
    bool keepdim=false,
    bool upcast=false,
    CudaTensor* result=nullptr,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);


CudaTensor* all(CudaTensor* tensor);


// namespace augpy
}


// AUGPY_REDUCE_H
#endif
