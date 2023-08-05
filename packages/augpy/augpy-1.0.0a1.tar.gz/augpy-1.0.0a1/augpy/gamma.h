#ifndef AUGPY_GAMMA_H
#define AUGPY_GAMMA_H


#include <cuda.h>
#include <cuda_runtime.h>
#include <vector>
#include "tensor.h"


namespace augpy {


CudaTensor* add_gamma(
    CudaTensor* imtensor,
    CudaTensor* gammagrays,
    CudaTensor* gammacolors,
    CudaTensor* contrasts,
    double maxv,
    CudaTensor* out
);


// namespace augpy
}


// AUGPY_GAMMA_H
#endif
