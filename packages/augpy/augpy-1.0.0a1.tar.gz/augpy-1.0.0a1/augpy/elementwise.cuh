#ifndef AUGPY_ELEMENTWISE_CUH
#define AUGPY_ELEMENTWISE_CUH

#include "tensor.h"


namespace augpy {


struct tensor_param {
    unsigned char* ptr;
    ndim_array strides;
};


template <int n_tensors, typename param_t,
          void (*F)(array<tensor_param, n_tensors>, param_t)>
__global__ void elementwise_contiguous_kernel(
        array<tensor_param, n_tensors> tensors,
        param_t constants,
        size_t contiguous_stride,
        const unsigned int values_per_thread,
        size_t shape0
){
    size_t rem = blockDim.x * blockIdx.x * values_per_thread + threadIdx.x;
    if (rem >= shape0) {
        return;
    }
    shape0 = min((size_t)values_per_thread, ceil_div(shape0 - rem, blockDim.x));
    // contiguous tensors will always be coalesced to 1D
    #pragma unroll
    for (int t=0; t<n_tensors; ++t) {
        tensors[t].ptr += rem * tensors[t].strides[0] / contiguous_stride;
    }

    // loop shape0 in dim 0
    for(; shape0>0; --shape0) {
        F(tensors, constants);
        #pragma unroll
        for (int i=0; i<n_tensors; ++i) {
            tensors[i].ptr += tensors[i].strides[0];
        }
    }
}


template <int n_tensors, typename param_t,
          void (*F)(array<tensor_param, n_tensors>, param_t)>
__global__ void elementwise_kernel(
        array<tensor_param, n_tensors> tensors,
        param_t constants,
        const ndim_array contiguous_strides,
        const int ndim,
        const size_t count,
        const unsigned int values_per_thread,
        size_t shape0
){
    // 0D and 1D tensors don't require translation
    if (ndim <= 1) {
        size_t rem = blockDim.x * blockIdx.x * values_per_thread + threadIdx.x;
        if (rem >= count) {
            return;
        }
        shape0 = min((size_t)values_per_thread, ceil_div(shape0 - rem, blockDim.x));
        #pragma unroll
        for (int t=0; t<n_tensors; ++t) {
            tensors[t].ptr += rem * tensors[t].strides[0] / contiguous_strides[0];
        }
    }
    // with ND tensors loop over dim 0
    // dim 0 is defined by blockIdx.x * values_per_thread
    // remainder of indices is translated through strides
    else {
        size_t rem = blockDim.x * blockIdx.y + threadIdx.x;
        if (rem >= count) {
            return;
        }
        // calculate the first dimension index
        size_t x = (size_t) blockIdx.x * values_per_thread;
        // remaining values in first dimension
        shape0 = min((size_t)values_per_thread, shape0 - x);
        // move pointers in first dimension
        #pragma unroll
        for (int t=0; t<n_tensors; ++t) {
            tensors[t].ptr += tensors[t].strides[0] * x;
        }
        // ensure ndim_arrays are put into registers instead of local memory:
        //  - loop must be fixed length so it can be unrolled,
        //    thus indexing arrays with a constant value
        //  - exit the loop manually by testing against ndim
        //
        // See this section of the CUDA programming guide for details:
        // https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#device-memory-accesses
        #pragma unroll
        for(int dim=1; dim<DLTENSOR_MAX_NDIM; ++dim) {
            if (dim >= ndim) break;
            size_t p = rem / contiguous_strides[dim];
            #pragma unroll
            for (int t=0; t<n_tensors; ++t) {
                tensors[t].ptr += p * tensors[t].strides[dim];
            }
            rem -= p * contiguous_strides[dim];
        }
    }

    // loop shape0 in dim 0
    for(; shape0>0; --shape0) {
        F(tensors, constants);
        #pragma unroll
        for (int i=0; i<n_tensors; ++i) {
            tensors[i].ptr += tensors[i].strides[0];
        }
    }
}


template <int n_tensors, typename param_t,
          void (*F)(array<tensor_param, n_tensors>, param_t)>
CudaTensor* elementwise_function(
        array<CudaTensor*, n_tensors> tensors,
        param_t constant,
        unsigned int blocks_per_sm,
        unsigned int num_threads,
        bool enforce_same_dtype=true
){
    static_assert(n_tensors >= 0, "need at least 1 output tensor");

    CudaTensor* retval = NULL;
    // create output tensor if none given
    // output shape is determined by broadcasting all input tensors
    if (!tensors[0]) {
        if (n_tensors <= 1) {
            throw std::invalid_argument("no output tensor given");
        }
        if (!tensors[1]) {
            throw std::invalid_argument("required argument 1 is None");
        }
        // make output tensor with max in every dimension of given tensors
        // requiring all tensors to not be NULL
        tensors[0] = retval = create_output_tensor(&tensors[1], n_tensors-1, false);
    }

    // fill dltensors and tensor_params with current values
    array<ndim_array, n_tensors> shapes;
    array<tensor_param, n_tensors> tensor_params;
    std::vector<DLTensor> dltensors(n_tensors);
    for (int t=0; t<n_tensors; ++t) {
        DLTensor dlt = tensors[t]->dl_tensor;
        shapes[t] = ndim_array(dlt.shape, dlt.ndim);
        tensor_params[t].strides = ndim_array(dlt.strides, dlt.ndim);
        tensor_params[t].ptr = reinterpret_cast<unsigned char*>(tensors[t]->ptr());
        dlt.shape = &shapes[t][0];
        dlt.strides = &tensor_params[t].strides[0];
        dltensors[t] = dlt;
    }

    // attempt to broadcast every tensor to output shape
    // filling the tensor_param array in the process
    DLTensor &r = dltensors[0];
    bool broadcast = false;
    for (int t=0; t<n_tensors; ++t) {
        if (enforce_same_dtype) {
            check_same_dtype_device(dltensors[t], r);
        }
        else {
            check_same_device(dltensors[t], r);
        }
        broadcast = calculate_broadcast_strides(dltensors[t], r, tensor_params[t].strides, t);
    }

    // attempt to coalesce dimensions and calculate contiguous strides
    coalesce_dimensions(dltensors);
    ndim_array contiguous_strides;
    calculate_contiguous_strides(r, contiguous_strides);

    // so far shapes of tensors in call were compatible
    // if numel(tensor)==0 for some tensor, there is nothing to do
    for (int t=0; t<n_tensors; ++t) {
        if (numel(tensors[t]->dl_tensor) == 0) {
            return retval;
        }
    }

    // check if all tensors are contiguous
    bool contiguous = !broadcast;
    for (int t=0; t<n_tensors; ++t) {
        if (!contiguous) break;
        contiguous = tensors[t]->is_contiguous();
    }

    // determine the launch configuration
    calc_threads(num_threads, r.ctx.device_id);
    dim3 grid(1, 1, 1);
    size_t count;
    int64_t shape0;
    unsigned int values_per_thread = 0;
    // result is a scalar
    if (r.ndim == 0) {
        count = 1;
        shape0 = 1;
        num_threads = 1;
        values_per_thread = 1;
        contiguous_strides[0] = 1;
        contiguous = true;
    }
    // result is 1D
    else if (r.ndim == 1) {
        shape0 = r.shape[0];
        calc_blocks_values_1d(r, grid.x, count, values_per_thread, num_threads, blocks_per_sm);
        // every thread will stride by block size = num_threads
        for (int t=0; t<n_tensors; ++t) {
            tensor_params[t].strides[0] *= num_threads;
        }
        contiguous_strides[0] *= num_threads;
    }
    // result is ND
    else {
        shape0 = r.shape[0];
        calc_blocks_values_nd(r, grid, count, values_per_thread, num_threads, blocks_per_sm);
    }

    // DLTensor strides are defined as items
    // elementwise_kernel assumes all strides are given in bytes
    // multiply all strides by number of bytes in dtype
    for (int t=0; t<n_tensors; ++t) {
        int bytes = itemsize(dltensors[t].dtype);
        for (int dim=0; dim<r.ndim; ++dim) {
            tensor_params[t].strides[dim] *= bytes;
        }
    }

    /*printf("launch config: grid(%d, %d, %d), num_threads %d, count %ld, values_per_thread %d\n",
           grid.x, grid.y, grid.z, num_threads, count, values_per_thread);
    printf("contiguous strides: ");
    for (int dim=0; dim<DLTENSOR_MAX_NDIM; ++dim) {
        printf("dim %d (strides %ld), ", dim, contiguous_strides[dim]);
    }
    printf("\n");
    for (int t=0; t<n_tensors; ++t) {
        printf("tensor %d: ", t);
        DLTensor dlt = dltensors[t];
        for (int dim=0; dim<DLTENSOR_MAX_NDIM; ++dim) {
            printf("dim %d (shape %ld, strides %ld), ", dim, dlt.shape[dim], dlt.strides[dim]);
        }
        printf("\n");
    }*/

    // launch contiguous kernel
    if (contiguous) {
        //printf("contiguous\n");
        elementwise_contiguous_kernel<n_tensors, param_t, F>
        <<<grid, num_threads, 0, current_stream>>>(
            tensor_params, constant, contiguous_strides[0], values_per_thread, shape0
        );
    }
    // launch strided kernel
    else {
        //printf("strided\n");
        elementwise_kernel<n_tensors, param_t, F>
        <<<grid, num_threads, 0, current_stream>>>(
            tensor_params, constant, contiguous_strides,
            r.ndim, count, values_per_thread, shape0
        );
    }

    CUDA(cudaGetLastError());

    // record usage of involved tensors
    for (int t=0; t<n_tensors; ++t) {
        tensors[t]->record();
    }

    return retval;
}


// namespace augpy
}


// AUGPY_ELEMENTWISE_CUH
#endif
