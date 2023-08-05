#include <cuda.h>
#include <cuda_runtime.h>
#include "tensor.h"
#include "dispatch.h"
#include "saturate_cast.cuh"
#include "elementwise.cuh"
#include <tuple>
#include <algorithm>


namespace augpy {


CudaTensor* make_result_tensor(CudaTensor* tensor, CudaTensor** result) {
    if (!tensor) {
        throw std::invalid_argument("argument 1 may not be None");
    }
    DLTensor t = tensor->dl_tensor;
    CudaTensor* retval = nullptr;
    if (!*result) {
        *result = retval = new CudaTensor(t.shape, t.ndim, dldtype_uint8, t.ctx.device_id);
    }
    return retval;
}


CudaTensor* make_result_tensor(CudaTensor* tensor1, CudaTensor* tensor2, CudaTensor** result) {
    if (!tensor1 || !tensor2) {
        throw std::invalid_argument("argument 1 and 2 may not be None");
    }
    DLTensor t1 = tensor1->dl_tensor;
    DLTensor t2 = tensor2->dl_tensor;
    check_same_dtype_device(t1, t2);
    CudaTensor* retval = nullptr;
    if (!*result) {
        int ndim;
        ndim_array shape;
        calculate_broadcast_output_shape(t1, t2, ndim, shape);
        *result = retval = new CudaTensor(shape.ptr(), ndim, dldtype_uint8, t1.ctx.device_id);
    }
    return retval;
}


template <typename scalar_t>
__device__ __forceinline__ void __lt(
        array<tensor_param, 2> tensors,
        scalar_t scalar
){
    *reinterpret_cast<uint8_t*>(tensors[0].ptr) = 
        (*reinterpret_cast<scalar_t*>(tensors[1].ptr) < scalar);
}


template <typename scalar_t>
__device__ __forceinline__ void __le(
        array<tensor_param, 2> tensors,
        scalar_t scalar
){
    *reinterpret_cast<uint8_t*>(tensors[0].ptr) = 
        *reinterpret_cast<scalar_t*>(tensors[1].ptr) <= scalar;
}


template <typename scalar_t>
__device__ __forceinline__ void __gt(
        array<tensor_param, 2> tensors,
        scalar_t scalar
){
    *reinterpret_cast<uint8_t*>(tensors[0].ptr) = 
        (*reinterpret_cast<scalar_t*>(tensors[1].ptr) > scalar);
}


template <typename scalar_t>
__device__ __forceinline__ void __ge(
        array<tensor_param, 2> tensors,
        scalar_t scalar
){
    *reinterpret_cast<uint8_t*>(tensors[0].ptr) = 
        *reinterpret_cast<scalar_t*>(tensors[1].ptr) >= scalar;
}


template <typename scalar_t>
__device__ __forceinline__ void __eq(
        array<tensor_param, 2> tensors,
        scalar_t scalar
){
    *reinterpret_cast<uint8_t*>(tensors[0].ptr) = 
        *reinterpret_cast<scalar_t*>(tensors[1].ptr) == scalar;
}


template<typename scalar_t>
__device__ __forceinline__ void __lt_tensor(
        array<tensor_param, 3> tensors,
        uint8_t nothing
){
    *reinterpret_cast<uint8_t*>(tensors[0].ptr) = 
        *reinterpret_cast<scalar_t*>(tensors[1].ptr) <
        *reinterpret_cast<scalar_t*>(tensors[2].ptr);
}


template<typename scalar_t>
__device__ __forceinline__ void __le_tensor(
        array<tensor_param, 3> tensors,
        uint8_t nothing
){
    *reinterpret_cast<uint8_t*>(tensors[0].ptr) = 
        *reinterpret_cast<scalar_t*>(tensors[1].ptr) <
        *reinterpret_cast<scalar_t*>(tensors[2].ptr);
}


template<typename scalar_t>
__device__ __forceinline__ void __eq_tensor(
        array<tensor_param, 3> tensors,
        uint8_t nothing
){
    *reinterpret_cast<uint8_t*>(tensors[0].ptr) = 
        *reinterpret_cast<scalar_t*>(tensors[1].ptr) ==
        *reinterpret_cast<scalar_t*>(tensors[2].ptr);
}


CudaTensor* lt_scalar(
        CudaTensor* tensor,
        double scalar,
        CudaTensor* result,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    CudaTensor* retval = make_result_tensor(tensor, &result);
    auto tensors = make_array(result, tensor);
    DISPATCH(tensor->dl_tensor.dtype, "lt_scalar", ([&] {
        scalar_t casted;
        saturate_cast<double, scalar_t>(scalar, &casted);
        retval = elementwise_function<2, scalar_t, __lt<scalar_t>>(
            tensors, casted, blocks_per_sm, num_threads, false
        );
    }));
    return result;
}


CudaTensor* le_scalar(
        CudaTensor* tensor,
        double scalar,
        CudaTensor* result,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    CudaTensor* retval = make_result_tensor(tensor, &result);
    auto tensors = make_array(result, tensor);
    DISPATCH(tensor->dl_tensor.dtype, "lt_scalar", ([&] {
        scalar_t casted;
        saturate_cast<double, scalar_t>(scalar, &casted);
        retval = elementwise_function<2, scalar_t, __le<scalar_t>>(
            tensors, casted, blocks_per_sm, num_threads, false
        );
    }));
    return result;
}


CudaTensor* gt_scalar(
        CudaTensor* tensor,
        double scalar,
        CudaTensor* result,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    CudaTensor* retval = make_result_tensor(tensor, &result);
    auto tensors = make_array(result, tensor);
    DISPATCH(tensor->dl_tensor.dtype, "lt_scalar", ([&] {
        scalar_t casted;
        saturate_cast<double, scalar_t>(scalar, &casted);
        retval = elementwise_function<2, scalar_t, __gt<scalar_t>>(
            tensors, casted, blocks_per_sm, num_threads, false
        );
    }));
    return result;
}


CudaTensor* ge_scalar(
        CudaTensor* tensor,
        double scalar,
        CudaTensor* result,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    CudaTensor* retval = make_result_tensor(tensor, &result);
    auto tensors = make_array(result, tensor);
    DISPATCH(tensor->dl_tensor.dtype, "lt_scalar", ([&] {
        scalar_t casted;
        saturate_cast<double, scalar_t>(scalar, &casted);
        retval = elementwise_function<2, scalar_t, __ge<scalar_t>>(
            tensors, casted, blocks_per_sm, num_threads, false
        );
    }));
    return result;
}


CudaTensor* eq_scalar(
        CudaTensor* tensor,
        double scalar,
        CudaTensor* result,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    CudaTensor* retval = make_result_tensor(tensor, &result);
    auto tensors = make_array(result, tensor);
    DISPATCH(tensor->dl_tensor.dtype, "lt_scalar", ([&] {
        scalar_t casted;
        saturate_cast<double, scalar_t>(scalar, &casted);
        retval = elementwise_function<2, scalar_t, __eq<scalar_t>>(
            tensors, casted, blocks_per_sm, num_threads, false
        );
    }));
    return result;
}


CudaTensor* lt_tensor(
        CudaTensor* tensor1,
        CudaTensor* tensor2,
        CudaTensor* result,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    CudaTensor* retval = make_result_tensor(tensor1, tensor2, &result);
    auto tensors = make_array(result, tensor1, tensor2);
    DISPATCH(tensor1->dl_tensor.dtype, "add_scaled_tensor", ([&] {
        retval = elementwise_function<3, uint8_t, __lt_tensor<scalar_t>>(
            tensors, 0, blocks_per_sm, num_threads, false
        );
    }));
    return retval;
}


CudaTensor* le_tensor(
        CudaTensor* tensor1,
        CudaTensor* tensor2,
        CudaTensor* result,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    CudaTensor* retval = make_result_tensor(tensor1, tensor2, &result);
    auto tensors = make_array(result, tensor1, tensor2);
    DISPATCH(tensor1->dl_tensor.dtype, "add_scaled_tensor", ([&] {
        retval = elementwise_function<3, uint8_t, __le_tensor<scalar_t>>(
            tensors, 0, blocks_per_sm, num_threads, false
        );
    }));
    return retval;
}


CudaTensor* eq_tensor(
        CudaTensor* tensor1,
        CudaTensor* tensor2,
        CudaTensor* result,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    CudaTensor* retval = make_result_tensor(tensor1, tensor2, &result);
    auto tensors = make_array(result, tensor1, tensor2);
    DISPATCH(tensor1->dl_tensor.dtype, "add_scaled_tensor", ([&] {
        retval = elementwise_function<3, uint8_t, __eq_tensor<scalar_t>>(
            tensors, 0, blocks_per_sm, num_threads, false
        );
    }));
    return retval;
}


// namespace augpy
}
