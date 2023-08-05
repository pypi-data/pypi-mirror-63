// blur.h
#ifndef CUDA_BLUR_H
#define CUDA_BLUR_H


#include <vector>


namespace augpy {


CudaTensor* box_blur_single(
        CudaTensor* input,
        int ksize,
        CudaTensor* out
);


CudaTensor* gaussian_blur(
        CudaTensor* input,
        CudaTensor* sigmas,
        int max_ksize,
        CudaTensor* out
);


CudaTensor* gaussian_blur_single(
        CudaTensor* input,
        float sigma,
        CudaTensor* out
);


// namespace augpy
}


// blur.h
#endif
