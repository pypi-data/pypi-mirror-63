#include <cuda.h>
#include <cuda_runtime.h>
#include "tensor.h"
#include "dispatch.h"
#include "saturate_cast.cuh"
#include "elementwise.cuh"
#include <tuple>


template<typename scalar_t>
__device__ __forceinline__ scalar_t generic_fma(scalar_t x, scalar_t y, scalar_t z);


template<>
__device__ __forceinline__ float generic_fma(float x, float y, float z){
    return fmaf(x,y,z);
}


template<>
__device__ __forceinline__ double generic_fma(double x, double y, double z){
    return fma(x,y,z);
}


namespace augpy {


template <typename scalar_t, typename sscalar_t, typename temp_t>
__device__ __forceinline__ void fma_function(
        array<tensor_param, 3> tensors,
        temp_t scalar
){
    saturate_cast<temp_t, scalar_t>(generic_fma(
        scalar,
        (temp_t) *reinterpret_cast<sscalar_t*>(tensors[1].ptr),
        (temp_t) *reinterpret_cast<scalar_t*>(tensors[2].ptr)
    ), reinterpret_cast<scalar_t*>(tensors[0].ptr));
}


CudaTensor* fma(
        double scalar,
        CudaTensor* tensor1,
        CudaTensor* tensor2,
        CudaTensor* result,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    CudaTensor* retval = NULL;
    auto tensors = make_array(result, tensor1, tensor2);
    DISPATCH(tensor2->dl_tensor.dtype, "fma", ([&] {
        ASSERT_TRUE(dldatatype_equals(get_dldatatype<sscalar_t>(), tensor1->dl_tensor.dtype),
                    "tensor1 dtype must be signed version of tensor2 dtype");
        if (result) {
            ASSERT_TRUE(dldatatype_equals(tensor2->dl_tensor.dtype, tensor2->dl_tensor.dtype),
                        "tensor2 dtype must same as result tensor");
        }
        retval = elementwise_function<3, temp_t, fma_function<scalar_t, sscalar_t, temp_t>>(
            tensors,
            (temp_t) scalar,
            blocks_per_sm,
            num_threads
        );
    }));
    return retval;
}


template <typename scalar_t, typename temp_t>
__device__ __forceinline__ void __add_scaled(
        array<tensor_param, 2> tensors,
        std::tuple<temp_t, temp_t> scalars
){
    saturate_cast<temp_t, scalar_t>(generic_fma(
        std::get<1>(scalars),
        (temp_t) *reinterpret_cast<scalar_t*>(tensors[1].ptr),
        std::get<0>(scalars)
    ), reinterpret_cast<scalar_t*>(tensors[0].ptr));
}


CudaTensor* add_scaled(
        double alpha,
        double beta,
        CudaTensor* tensor,
        CudaTensor* result,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    CudaTensor* retval = NULL;
    auto tensors = make_array(result, tensor);
    DISPATCH(tensor->dl_tensor.dtype, "add_scaled", ([&] {
        retval = elementwise_function<2, std::tuple<temp_t, temp_t>, __add_scaled<scalar_t, temp_t>>(
            tensors,
            std::make_tuple((temp_t)alpha, (temp_t)beta),
            blocks_per_sm,
            num_threads
        );
    }));
    return retval;
}


template<typename scalar_t, typename temp_t>
__device__ __forceinline__ void __add_scaled_tensor(
        array<tensor_param, 3> tensors,
        std::tuple<temp_t> scalars
){
    saturate_cast<temp_t, scalar_t>(generic_fma(
        std::get<0>(scalars),
        (temp_t) *reinterpret_cast<scalar_t*>(tensors[1].ptr),
        (temp_t) *reinterpret_cast<scalar_t*>(tensors[2].ptr)
    ), reinterpret_cast<scalar_t*>(tensors[0].ptr));
}


CudaTensor* add_scaled_tensor(
        double alpha,
        CudaTensor* tensor1,
        CudaTensor* tensor2,
        CudaTensor* result,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    CudaTensor* retval = NULL;
    auto tensors = make_array(result, tensor1, tensor2);
    DISPATCH(tensor1->dl_tensor.dtype, "add_scaled_tensor", ([&] {
        retval = elementwise_function<3, std::tuple<temp_t>,
                                      __add_scaled_tensor<scalar_t, temp_t>>(
            tensors,
            std::make_tuple((temp_t)alpha),
            blocks_per_sm,
            num_threads
        );
    }));
    return retval;
}


template<typename scalar_t, typename temp_t>
__device__ __forceinline__ void __mul_scaled_tensor(
        array<tensor_param, 3> tensors,
        std::tuple<temp_t> scalars
){
    saturate_cast<temp_t, scalar_t>(generic_fma(
        (temp_t) *reinterpret_cast<scalar_t*>(tensors[1].ptr),
        (temp_t) *reinterpret_cast<scalar_t*>(tensors[2].ptr),
        std::get<0>(scalars)
    ), reinterpret_cast<scalar_t*>(tensors[0].ptr));
}


CudaTensor* mul_scaled_tensor(
        double alpha, CudaTensor* tensor1, CudaTensor* tensor2, CudaTensor* result,
        unsigned int blocks_per_sm, unsigned int num_threads
){
    CudaTensor* retval = NULL;
    auto tensors = make_array(result, tensor1, tensor2);
    DISPATCH(tensor1->dl_tensor.dtype, "mul_scaled_tensor", ([&] {
        retval = elementwise_function<3, std::tuple<temp_t>,
                                      __mul_scaled_tensor<scalar_t, temp_t>>(
            tensors,
            std::make_tuple((temp_t)alpha),
            blocks_per_sm,
            num_threads
        );
    }));
    return retval;
}


template<typename scalar_t, typename temp_t>
__device__ __forceinline__ void __rdiv_scaled(
        array<tensor_param, 2> tensors,
        std::tuple<temp_t, temp_t> scalars
){
    saturate_cast<temp_t, scalar_t>(
        std::get<0>(scalars)
        + std::get<1>(scalars) / (temp_t) *reinterpret_cast<scalar_t*>(tensors[1].ptr),
        reinterpret_cast<scalar_t*>(tensors[0].ptr)
    );
}


CudaTensor* rdiv_scaled(
        double alpha, double beta, CudaTensor* tensor, CudaTensor* result,
        unsigned int blocks_per_sm, unsigned int num_threads
){
    CudaTensor* retval = NULL;
    auto tensors = make_array(result, tensor);
    DISPATCH(tensor->dl_tensor.dtype, "rdiv_scaled", ([&] {
        retval = elementwise_function<2, std::tuple<temp_t, temp_t>,
                                      __rdiv_scaled<scalar_t, temp_t>>(
            tensors,
            std::make_tuple((temp_t)alpha, (temp_t)beta),
            blocks_per_sm,
            num_threads
        );
    }));
    return retval;
}


template<typename scalar_t, typename temp_t>
__device__ __forceinline__ void __div_scaled_tensor(
        array<tensor_param, 3> tensors,
        std::tuple<temp_t, temp_t> scalars
){
    saturate_cast<temp_t, scalar_t>(
        generic_fma(
            std::get<1>(scalars),
            (temp_t) *reinterpret_cast<scalar_t*>(tensors[1].ptr),
            std::get<0>(scalars)
        ) / (temp_t) *reinterpret_cast<scalar_t*>(tensors[2].ptr),
    reinterpret_cast<scalar_t*>(tensors[0].ptr));
}


CudaTensor* div_scaled_tensor(
        double alpha, double beta, CudaTensor* tensor1, CudaTensor* tensor2, CudaTensor* result,
        unsigned int blocks_per_sm, unsigned int num_threads
){
    CudaTensor* retval = NULL;
    auto tensors = make_array(result, tensor1, tensor2);
    DISPATCH(tensor1->dl_tensor.dtype, "rdiv_scaled", ([&] {
        retval = elementwise_function<3, std::tuple<temp_t, temp_t>,
                                      __div_scaled_tensor<scalar_t, temp_t>>(
            tensors,
            std::make_tuple((temp_t)alpha, (temp_t)beta),
            blocks_per_sm,
            num_threads
        );
    }));
    return retval;
}


CudaTensor* add_scalar(
        CudaTensor* tensor, double scalar, CudaTensor* result,
        unsigned int blocks_per_sm, unsigned int num_threads
){
    return add_scaled(scalar, 1.0, tensor, result,
                      blocks_per_sm, num_threads);
}


CudaTensor* sub_scalar(
        CudaTensor* tensor, double scalar, CudaTensor* result,
        unsigned int blocks_per_sm, unsigned int num_threads
){
    return add_scaled(-scalar, 1.0, tensor, result,
                      blocks_per_sm, num_threads);
}


CudaTensor* rsub_scalar(
        CudaTensor* tensor, double scalar, CudaTensor* result,
        unsigned int blocks_per_sm, unsigned int num_threads
){
    return add_scaled(scalar, -1.0, tensor, result,
                      blocks_per_sm, num_threads);
}


CudaTensor* mul_scalar(
        CudaTensor* tensor, double scalar, CudaTensor* result,
        unsigned int blocks_per_sm, unsigned int num_threads
){
    return add_scaled(0.0, scalar, tensor, result,
                      blocks_per_sm, num_threads);
}


CudaTensor* div_scalar(
        CudaTensor* tensor, double scalar, CudaTensor* result,
        unsigned int blocks_per_sm, unsigned int num_threads
){
    return add_scaled(0.0, 1.0/scalar, tensor, result,
                      blocks_per_sm, num_threads);
}


CudaTensor* rdiv_scalar(
        CudaTensor* tensor, double scalar, CudaTensor* result,
        unsigned int blocks_per_sm, unsigned int num_threads
){
    return rdiv_scaled(0.0, scalar, tensor, result,
                       blocks_per_sm, num_threads);
}


CudaTensor* add_tensor(
    CudaTensor* tensor1, CudaTensor* tensor2, CudaTensor* result,
    unsigned int blocks_per_sm, unsigned int num_threads
){
    return add_scaled_tensor(1.0, tensor1, tensor2, result,
                             blocks_per_sm, num_threads);
}


CudaTensor* sub_tensor(
    CudaTensor* tensor1, CudaTensor* tensor2, CudaTensor* result,
    unsigned int blocks_per_sm, unsigned int num_threads
){
    return add_scaled_tensor(-1.0, tensor2, tensor1, result,
                             blocks_per_sm, num_threads);
}


CudaTensor* mul_tensor(
    CudaTensor* tensor1, CudaTensor* tensor2, CudaTensor* result,
    unsigned int blocks_per_sm, unsigned int num_threads
){
    return mul_scaled_tensor(0.0, tensor1, tensor2, result,
                             blocks_per_sm, num_threads);
}


CudaTensor* div_tensor(
    CudaTensor* tensor1, CudaTensor* tensor2, CudaTensor* result,
    unsigned int blocks_per_sm, unsigned int num_threads
){
    return div_scaled_tensor(0.0, 1.0, tensor1, tensor2, result,
                             blocks_per_sm, num_threads);
}


// namespace augpy
}
