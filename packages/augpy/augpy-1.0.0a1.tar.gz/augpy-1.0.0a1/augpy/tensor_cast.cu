#include <cuda.h>
#include <cuda_runtime.h>
#include "tensor.h"
#include "dispatch.h"
#include "saturate_cast.cuh"
#include "elementwise.cuh"
#include <tuple>


namespace augpy {


__device__ __forceinline__ void cast_function(
        array<tensor_param, 2> tensors,
        std::tuple<DLDataType, DLDataType> dtypes
){
    __DISPATCH_NOEXC(std::get<0>(dtypes), dst_t, "cast", ([&] {
        __DISPATCH_NOEXC(std::get<1>(dtypes), src_t, "cast", ([&] {
            saturate_cast<src_t, dst_t>(
                *reinterpret_cast<src_t*>(tensors[1].ptr),
                reinterpret_cast<dst_t*>(tensors[0].ptr)
            );
        }));
    }));
}


void cast_tensor(
        CudaTensor* src,
        CudaTensor* dst,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    if (!src || !dst) {
        throw std::invalid_argument("source and result tensor need to be a valid tensors");
    }
    DLTensor &t_src = src->dl_tensor;
    DLTensor &t_dst = dst->dl_tensor;
    if (t_src.ndim != t_dst.ndim || !array_equals(0, t_src.ndim, t_src.shape, t_dst.shape)) {
        throw std::invalid_argument("source and result tensor must have same shape");
    }
    auto tensors = make_array(dst, src);
    auto dtypes = std::make_tuple(t_dst.dtype, t_src.dtype);
    elementwise_function<2, std::tuple<DLDataType, DLDataType>, cast_function>(
        tensors, dtypes, blocks_per_sm, num_threads, false
    );
}


CudaTensor* cast_type(
        CudaTensor* tensor,
        DLDataType dtype,
        unsigned int blocks_per_sm,
        unsigned int num_threads
){
    DLTensor &t = tensor->dl_tensor;
    CudaTensor* out = new CudaTensor(&t.shape[0], t.ndim, dtype, t.ctx.device_id);
    cast_tensor(tensor, out, blocks_per_sm, num_threads);
    return out;
}


// namespace augpy
}
