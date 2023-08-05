#include <cuda.h>
#include <cuda_runtime.h>
#include "tensor.h"
#include "dispatch.h"
#include "elementwise.cuh"
#include "saturate_cast.cuh"


namespace augpy {


template<typename scalar_t>
__device__ __forceinline__ void copy_function(
        array<tensor_param, 2> tensors,
        unsigned char nothing
){
    *reinterpret_cast<scalar_t*>(tensors[0].ptr) = *reinterpret_cast<scalar_t*>(tensors[1].ptr);
}


CudaTensor* copy(
        CudaTensor* src,
        CudaTensor* dst,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    CudaTensor* retval = NULL;
    auto tensors = make_array(dst, src);
    DISPATCH(src->dl_tensor.dtype, "copy", ([&] {
        retval = elementwise_function<2, unsigned char, copy_function<scalar_t>>(
            tensors, 0, blocks_per_sm, num_threads
        );
    }));
    return retval;
}


template<typename scalar_t>
__device__ __forceinline__ void fill_function(
        array<tensor_param, 1> tensors,
        scalar_t fill_value
){
    *reinterpret_cast<scalar_t*>(tensors[0].ptr) = fill_value;
}


void fill(
        double scalar,
        CudaTensor* dst,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    auto tensors = make_array(dst);
    DISPATCH(dst->dl_tensor.dtype, "fill", ([&] {
        scalar_t casted_scalar;
        saturate_cast<double, scalar_t>(scalar, &casted_scalar);
        elementwise_function<1, scalar_t, fill_function<scalar_t>>(
            tensors, casted_scalar, blocks_per_sm, num_threads
        );
    }));
}


// namespace augpy
}
