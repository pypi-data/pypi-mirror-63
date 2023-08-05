#include <cuda.h>
#include <cuda_runtime.h>
#include "tensor.h"
#include "dispatch.h"
#include "saturate_cast.cuh"
#include "elementwise.cuh"
#include "cub/device/device_reduce.cuh"
#include "cub/iterator/transform_input_iterator.cuh"


namespace augpy {


// logical AND operator
template<typename temp_t>
struct SaturatedSum
{
    template <typename scalar_t>
    __device__ __forceinline__
    scalar_t operator()(const scalar_t &a, const scalar_t &b) const {
        scalar_t result;
        saturate_cast<temp_t, scalar_t>((temp_t)a + (temp_t)b, &result);
        return result;
    }
};


CudaTensor* sum(
        CudaTensor* tensor,
        bool upcast
){
    if (!tensor->is_contiguous()) {
        throw std::invalid_argument("input must be contiguous");
    }
    DLTensor& t = tensor->dl_tensor;
    size_t num_items = numel(t);
    size_t temp_storage_bytes;
    CudaTensor* temp=nullptr;
    CudaTensor* out=nullptr;
    cudaError_t e;
    DISPATCH(t.dtype, "sum_kernel", ([&] {
        // interator that casts to temp_t
        cub::CastOp<temp_t> op_cast;
        cub::TransformInputIterator<double, cub::CastOp<temp_t>, scalar_t*> it_cast(
            (scalar_t*)tensor->ptr(), op_cast
        );
        // get required temp storage size
        CUDA(cub::DeviceReduce::Sum(
            nullptr, temp_storage_bytes,
            (scalar_t*) nullptr, (temp_t*) nullptr,
            num_items
        ));
        int64_t tsb = (int64_t) temp_storage_bytes;
        temp = new CudaTensor(&tsb, 1, dldtype_uint8, current_device);
        // sum with upcast to temp_t
        out = new CudaTensor(nullptr, 0, get_dldatatype<temp_t>(), current_device);
        e = cub::DeviceReduce::Sum(
            temp->ptr(),
            temp_storage_bytes,
            it_cast,
            (temp_t*) out->ptr(),
            num_items,
            current_stream
        );
    }));
    if (e==cudaSuccess) {
        temp->record();
    }
    if (temp) {
        delete temp;
    }
    if (e!=cudaSuccess) {
        if (out) {
            delete out;
        }
        CUDA(e);
    }
    if (!upcast) {
        temp = cast_type(out, t.dtype);
        delete out;
        out = temp;
    }
    return out;
}


template <typename scalar_t, typename temp_t>
__device__ __forceinline__ void __sum_axis_sat(
        array<tensor_param, 2> tensors,
        std::tuple<int64_t, int64_t> params
){
    temp_t v = 0;
    for(int64_t count=0; count<std::get<0>(params); ++count) {
        v += (temp_t) *reinterpret_cast<scalar_t*>(tensors[1].ptr);
        tensors[1].ptr += std::get<1>(params);
    }
    saturate_cast<temp_t, scalar_t>(v, reinterpret_cast<scalar_t*>(tensors[0].ptr));
}


template <typename scalar_t, typename temp_t>
__device__ __forceinline__ void __sum_axis_cast(
        array<tensor_param, 2> tensors,
        std::tuple<int64_t, int64_t> params
){
    temp_t v = 0;
    for(int64_t count=0; count<std::get<0>(params); ++count) {
        v += (temp_t) *reinterpret_cast<scalar_t*>(tensors[1].ptr);
        tensors[1].ptr += std::get<1>(params);
    }
    *reinterpret_cast<temp_t*>(tensors[0].ptr) = v;
}


CudaTensor* sum_axis(
        CudaTensor* tensor,
        int axis,
        bool keepdim,
        bool upcast,
        CudaTensor* result,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    DLTensor& t = tensor->dl_tensor;
    if (axis < 0 || axis >= t.ndim) {
        throw std::invalid_argument("axis out of range");
    }
    int64_t new_shape[DLTENSOR_MAX_NDIM];
    int64_t new_strides[DLTENSOR_MAX_NDIM];
    int new_ndim = 0;
    for (int dim=0; dim<t.ndim; ++dim) {
        if (dim == axis) {
            if (keepdim) {
                new_shape[new_ndim] = 1;
                new_strides[new_ndim] = 1;
                ++new_ndim;
            }
        }
        else {
            new_shape[new_ndim] = t.shape[dim];
            new_strides[new_ndim] = t.strides[dim];
            ++new_ndim;
        }
    }
    CudaTensor tensor_noaxis(tensor, new_ndim, new_shape, new_strides, 0);
    CudaTensor* retval = nullptr;
    DISPATCH(tensor->dl_tensor.dtype, "sum_axis", ([&] {
        // sum with upcast to temp_t
        if (upcast) {
            if (!result) {
                retval = result = new CudaTensor(
                    tensor_noaxis.dl_tensor.shape,
                    tensor_noaxis.dl_tensor.ndim,
                    get_dldatatype<temp_t>(),
                    tensor_noaxis.dl_tensor.ctx.device_id
                );
            }
            elementwise_function<2, std::tuple<int64_t, int64_t>, __sum_axis_cast<scalar_t, temp_t>>(
                make_array(result, &tensor_noaxis),
                std::make_tuple(t.shape[axis], t.strides[axis] * itemsize(t.dtype)),
                blocks_per_sm, num_threads, false
            );
        }
        // saturating sum
        else {
            if (!result) {
                retval = result = new CudaTensor(
                    tensor_noaxis.dl_tensor.shape,
                    tensor_noaxis.dl_tensor.ndim,
                    get_dldatatype<scalar_t>(),
                    tensor_noaxis.dl_tensor.ctx.device_id
                );
            }
            elementwise_function<2, std::tuple<int64_t, int64_t>, __sum_axis_sat<scalar_t, temp_t>>(
                make_array(result, &tensor_noaxis),
                std::make_tuple(t.shape[axis], t.strides[axis] * itemsize(t.dtype)),
                blocks_per_sm, num_threads, false
            );
        }

    }));
    return retval;
}


// logical AND operator
struct AndOp
{
    template <typename T>
    __device__ __forceinline__
    uint8_t operator()(const T &a, const T &b) const {
        return a && b;
    }
};


CudaTensor* all(CudaTensor* tensor) {
    DLTensor& t = tensor->dl_tensor;
    size_t num_items = numel(t);
    size_t temp_storage_bytes;
    CudaTensor* temp=nullptr;
    CudaTensor* out=nullptr;
    // call CUB
    cudaError_t e;
    AndOp op;
    DISPATCH(t.dtype, "all_kernel", ([&] {
        // get required temp storage size
        CUDA(cub::DeviceReduce::Reduce(
            nullptr, temp_storage_bytes,
            (scalar_t*) nullptr, (scalar_t*) nullptr,
            num_items, op, (uint8_t) 1
        ));
        // create temp storage and output
        int64_t tsb = (int64_t) temp_storage_bytes;
        temp = new CudaTensor(&tsb, 1, dldtype_uint8, current_device);
        out = new CudaTensor(nullptr, 0, dldtype_uint8, current_device);
        e = cub::DeviceReduce::Reduce(
            temp->ptr(),
            temp_storage_bytes,
            (scalar_t*) tensor->ptr(),
            (scalar_t*) out->ptr(),
            num_items,
            op,
            (uint8_t) 1,
            current_stream
        );
    }));
    if (e==cudaSuccess) {
        temp->record();
    }
    if (temp) {
        delete temp;
    }
    if (e!=cudaSuccess) {
        if (out) {
            delete out;
        }
        CUDA(e);
    }
    return out;
}


// namespace augpy
}
