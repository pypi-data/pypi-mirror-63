#ifndef AUGPY_TRANSLATE_IDX_CUH
#define AUGPY_TRANSLATE_IDX_CUH


#include "tensor.h"


namespace augpy {


template<typename scalar_t>
struct tensor_iterator{
    void* ptr;
    const size_t count;
    const int ndim;
    const ndim_array strides;
    const ndim_array contiguous_strides;

    tensor_iterator(void* ptr, int ndim, ndim_array strides, ndim_arry contiguous_strides): 
        ptr(ptr), count(count), ndim(ndim), strides(strides), contiguous_strides(contiguous_strides) {}

    scalar_t* operator[](size_t index) {
        void* t = ptr;
        // 1D tensors can use simple require translation
        if (ndim == 1) {
            if (index >= count) {
                return true;
            }
            t += index * strides[0] / contiguous_strides[0];
            return false;
        }
        // with ND tensors loop over dim 0
        // dim 0 is defined by blockIdx.x * values_per_thread
        // remainder of indices is translated through strides
        if (index >= count) {
            return true;
        }
        // calculate the first dimension index
        size_t x = (size_t) blockIdx.x * values_per_thread;
        // move pointers in first dimension
        t += strides[0] * x;
        // ensure ndim_arrays are put into registers instead of local memory:
        //  - loop must be fixed length so it can be unrolled,
        //    thus indexing arrays with a constant value
        //  - exit the loop manually by testing against ndim
        //
        // See this section of the CUDA programming guide for details:
        // https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#device-memory-accesses
        #pragma unroll
        for(int i=1; i<DLTENSOR_MAX_NDIM; ++i) {
            if (i >= ndim) break;
            size_t p = index / contiguous_strides[i];
            t += p * strides[i];
            index %= contiguous_strides[i];
        }
        return false;
    }
};


template<typename scalar_t>
__device__ __forceinline__ bool translate_idx_strided(
        scalar_t* &t,
        const ndim_array strides,
        const ndim_array contiguous_strides,
        const int ndim,
        const size_t count,
        const unsigned int values_per_thread,
        size_t &shape0
){
    // 1D tensors don't require translation
    if (ndim == 1) {
        size_t rem = blockDim.x * blockIdx.y * values_per_thread + threadIdx.x;
        if (rem >= count) {
            return true;
        }
        shape0 = min((size_t)values_per_thread, ceil_div(shape0 - rem, blockDim.x));
        t += rem * strides[0] / contiguous_strides[0];
        return false;
    }
    // with ND tensors loop over dim 0
    // dim 0 is defined by blockIdx.x * values_per_thread
    // remainder of indices is translated through strides
    size_t rem = blockDim.x * blockIdx.y + threadIdx.x;
    if (rem >= count) {
        return true;
    }
    // calculate the first dimension index
    size_t x = (size_t) blockIdx.x * values_per_thread;
    // remaining values in first dimension
    shape0 = min(x + values_per_thread, shape0) - x;
    // move pointers in first dimension
    t += strides[0] * x;
    // ensure ndim_arrays are put into registers instead of local memory:
    //  - loop must be fixed length so it can be unrolled,
    //    thus indexing arrays with a constant value
    //  - exit the loop manually by testing against ndim
    //
    // See this section of the CUDA programming guide for details:
    // https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#device-memory-accesses
    #pragma unroll
    for(int i=1; i<DLTENSOR_MAX_NDIM; ++i) {
        if (i >= ndim) break;
        size_t p = rem / contiguous_strides[i];
        t += p * strides[i];
        rem %= contiguous_strides[i];
    }
    return false;
}


template<typename scalar1_t, typename scalar2_t>
__device__ __forceinline__ bool translate_idx_contiguous_strided(
        scalar1_t* &t1,
        const ndim_array t1_strides,
        scalar2_t* &t2,
        const ndim_array t2_strides,
        const int ndim,
        const size_t count,
        const unsigned int values_per_thread,
        size_t &shape0
){
    // 1D tensors don't require translation
    if (ndim == 1) {
        size_t rem = blockDim.x * blockIdx.y * values_per_thread + threadIdx.x;
        if (rem >= count) {
            return true;
        }
        shape0 = min((size_t)values_per_thread, ceil_div(shape0 - rem, blockDim.x));
        t1 += rem;
        t2 += rem * t2_strides[0] / t1_strides[0];
        return false;
    }
    // with ND tensors loop over dim 0
    // dim 0 is defined by blockIdx.x * values_per_thread
    // remainder of indices is translated through strides
    size_t rem = blockDim.x * blockIdx.y + threadIdx.x;
    if (rem >= count) {
        return true;
    }
    // calculate the first dimension index
    size_t x = (size_t) blockIdx.x * values_per_thread;
    // remaining values in first dimension
    shape0 = min((size_t)values_per_thread, shape0 - x);
    // since t1 is contiguous, move t1 to final index
    t1 += t1_strides[0] * x + rem;
    // move t2 pointer in first dimension
    t2 += t2_strides[0] * x;
    // ensure ndim_arrays are put into registers instead of local memory:
    //  - loop must be fixed length so it can be unrolled,
    //    thus indexing arrays with a constant value
    //  - exit the loop manually by testing against ndim
    //
    // See this section of the CUDA programming guide for details:
    // https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#device-memory-accesses
    #pragma unroll
    for(int i=1; i<DLTENSOR_MAX_NDIM; ++i) {
        if (i >= ndim) break;
        t2 += rem / t1_strides[i] * t2_strides[i];
        rem %= t1_strides[i];
    }
    return false;
}


template<typename scalar1_t, typename scalar2_t>
__device__ __forceinline__ bool translate_idx_strided_strided(
        scalar1_t* &t1,
        const ndim_array t1_strides,
        scalar2_t* &t2,
        const ndim_array t2_strides,
        const ndim_array contiguous_strides,
        const int ndim,
        const size_t count,
        const unsigned int values_per_thread,
        size_t &shape0
){
    // 1D tensors don't require translation
    if (ndim == 1) {
        size_t rem = blockDim.x * blockIdx.y * values_per_thread + threadIdx.x;
        if (rem >= count) {
            return true;
        }
        shape0 = min((size_t)values_per_thread, ceil_div(shape0 - rem, blockDim.x));
        t1 += rem * t1_strides[0] / contiguous_strides[0];
        t2 += rem * t2_strides[0] / contiguous_strides[0];
        return false;
    }
    // with ND tensors loop over dim 0
    // dim 0 is defined by blockIdx.x * values_per_thread
    // remainder of indices is translated through strides
    size_t rem = blockDim.x * blockIdx.y + threadIdx.x;
    if (rem >= count) {
        return true;
    }
    // calculate the first dimension index
    size_t x = (size_t) blockIdx.x * values_per_thread;
    // remaining values in first dimension
    shape0 = min((size_t)values_per_thread, shape0 - x);
    // move pointers in first dimension
    t1 += t1_strides[0] * x;
    t2 += t2_strides[0] * x;
    // ensure ndim_arrays are put into registers instead of local memory:
    //  - loop must be fixed length so it can be unrolled,
    //    thus indexing arrays with a constant value
    //  - exit the loop manually by testing against ndim
    //
    // See this section of the CUDA programming guide for details:
    // https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#device-memory-accesses
    #pragma unroll
    for(int i=1; i<DLTENSOR_MAX_NDIM; ++i) {
        if (i >= ndim) break;
        size_t p = rem / contiguous_strides[i];
        t1 += p * t1_strides[i];
        t2 += p * t2_strides[i];
        rem %= contiguous_strides[i];
    }
    return false;
}


template<typename scalar1_t, typename scalar2_t, typename scalar3_t>
__device__ __forceinline__ bool translate_idx_strided_strided_strided(
        scalar1_t* &t1,
        const ndim_array t1_strides,
        scalar2_t* &t2,
        const ndim_array t2_strides,
        scalar3_t* &t3,
        const ndim_array t3_strides,
        const ndim_array contiguous_strides,
        const int ndim,
        const size_t count,
        const unsigned int values_per_thread,
        size_t &shape0
){
    // 1D tensors don't require translation
    if (ndim == 1) {
        size_t rem = blockDim.x * blockIdx.y * values_per_thread + threadIdx.x;
        if (rem >= count) {
            return true;
        }
        shape0 = min((size_t)values_per_thread, ceil_div(shape0 - rem, blockDim.x));
        t1 += rem * t1_strides[0] / contiguous_strides[0];
        t2 += rem * t2_strides[0] / contiguous_strides[0];
        t3 += rem * t3_strides[0] / contiguous_strides[0];
        return false;
    }
    // with ND tensors loop over dim 0
    // dim 0 is defined by blockIdx.x * values_per_thread
    // remainder of indices is translated through strides
    size_t rem = blockDim.x * blockIdx.y + threadIdx.x;
    if (rem >= count) {
        return true;
    }
    // calculate the first dimension index
    size_t x = (size_t) blockIdx.x * values_per_thread;
    // remaining values in first dimension
    shape0 = min((size_t)values_per_thread, shape0 - x);
    // move pointers in first dimension
    t1 += t1_strides[0] * x;
    t2 += t2_strides[0] * x;
    t3 += t3_strides[0] * x;
    // ensure ndim_arrays are put into registers instead of local memory:
    //  - loop must be fixed length so it can be unrolled,
    //    thus indexing arrays with a constant value
    //  - exit the loop manually by testing against ndim
    //
    // See this section of the CUDA programming guide for details:
    // https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#device-memory-accesses
    #pragma unroll
    for(int i=1; i<DLTENSOR_MAX_NDIM; ++i) {
        if (i >= ndim) break;
        size_t p = rem / contiguous_strides[i];
        t1 += p * t1_strides[i];
        t2 += p * t2_strides[i];
        t3 += p * t3_strides[i];
        rem %= contiguous_strides[i];
    }
    return false;
}




#define THREAD_LOOP_1(FUN, COUNTER, P1, STRIDE1) { \
    int64_t s1 = STRIDE1;                          \
    for(; COUNTER>0; --COUNTER) {                  \
        FUN;                                       \
        P1 += s1;                                  \
    }                                              \
}


#define THREAD_LOOP_2(FUN, COUNTER, P1, STRIDE1, P2, STRIDE2) { \
    int64_t s1 = STRIDE1, s2 = STRIDE2;                         \
    for(; COUNTER>0; --COUNTER) {                               \
        FUN;                                                    \
        P1 += s1;                                               \
        P2 += s2;                                               \
    }                                                           \
}


#define THREAD_LOOP_3(FUN, COUNTER, P1, STRIDE1, P2, STRIDE2, P3, STRIDE3) { \
    int64_t s1 = STRIDE1, s2 = STRIDE2, s3 = STRIDE3;                        \
    for(; COUNTER>0; --COUNTER) {                                            \
        FUN;                                                                 \
        P1 += s1;                                                            \
        P2 += s2;                                                            \
        P3 += s3;                                                            \
    }                                                                        \
}


// namespace augpy
}


// AUGPY_TRANSLATE_IDX_CUH
#endif
