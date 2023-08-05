#include <limits>
#include <cuda.h>
#include <cuda_runtime.h>
#include <curand.h>
#include <curand_kernel.h>
#include "core.h"
#include "tensor.h"
#include "saturate_cast.cuh"
#include "exception.h"
#include "dispatch.h"
#include "random.h"
#include <random>

#define EPSILON_FLOAT 1e-7
#define EPSILON_DOUBLE 1e-15
namespace augpy {


RandomNumberGenerator::RandomNumberGenerator(py::object* device_id_, py::object* seed_) {
    int new_device_id;
    int* device_id_p = NULL;
    unsigned long long new_seed;
    unsigned long long* seed_p = NULL;
    if (device_id_ && !device_id_->is_none()) {
        new_device_id = device_id_->cast<int>();
        device_id_p = &new_device_id;
    }
    if (seed_ && !seed_->is_none()) {
        new_seed = seed_->cast<unsigned long long>();
        seed_p = &new_seed;
    }
    init_device_state(device_id_p, seed_p);
}


RandomNumberGenerator::RandomNumberGenerator(int* device_id, unsigned long long* seed) {
    init_device_state(device_id, seed);
}


RandomNumberGenerator::~RandomNumberGenerator() noexcept(false) {
    if (device_states != NULL) {
        try {
            managed_cudafree(device_states);
        }
        // exceptions in destructor are not forwarded to Python,
        // so we cannot throw here :(
        catch (cnmem_error& e) {}
    }
}


template <typename rng_t>
__global__ void initialize_states_kernel(
    rng_t *state,
    size_t num_states,
    unsigned long long seed
) {
    unsigned long long sequence = blockDim.x * blockIdx.x + threadIdx.x;
    if (sequence < num_states) {
        curand_init(seed, sequence, 0, &state[sequence]);
    }
}


void RandomNumberGenerator::init_device_state(int* device_id_, unsigned long long* seed_) {
    // get default values
    if (!device_id_) {
        device_id_ = &current_device;
    }
    this->device_id = *device_id_;
    this->seed = 0;
    if (seed_) {
        this->seed = *seed_;
    }
    else {
        std::random_device initial;
        int steps = sizeof(unsigned long long) / sizeof(unsigned int);
        for (int i=0; i<steps; ++i) {
            seed <<= sizeof(unsigned int);
            seed += initial();
        }
    }

    // initialize state
    CUDA(cudaSetDevice(device_id));
    cudaDeviceProp props = get_device_properties(device_id);
    num_states = get_num_cuda_cores(device_id);
    size_t size = num_states * sizeof(rng_t);
    managed_cudamalloc((void **)&device_states, size, device_id);
    size_t num_blocks = ceil_div(num_states, 128);

    // retrieve the current stack limit, i.e.,
    // the number of bytes the stack of each thread can hold
    size_t stacklimit;
    CUDA(cudaDeviceGetLimit(&stacklimit, cudaLimitStackSize));

    // calls to curand_init may require a very large stack size,
    // thus increasing the reserved space in device memory
    initialize_states_kernel<rng_t><<<num_blocks, 128, 0, current_stream>>>(
        device_states, num_states, seed
    );

    // wait for random state initialization to finish
    // and reset stack limit back to previous value
    CUDA(cudaStreamSynchronize(current_stream));
    CUDA(cudaDeviceSetLimit(cudaLimitStackSize, stacklimit));
}


template<typename rng_t, typename scalar_t>
__device__ __forceinline__ scalar_t __curand_uniform(rng_t* state);

template<>
__device__ __forceinline__ float __curand_uniform(rng_t* state){
    return curand_uniform(state);
}

template<>
__device__ __forceinline__ double __curand_uniform(rng_t* state){
    return curand_uniform_double(state);
}


template<typename rng_t, typename scalar_t, typename temp_t>
__global__ void generate_uniform_kernel(
    scalar_t* result,
    const size_t n,
    const unsigned int m,
    const temp_t offset,
    const temp_t scale,
    rng_t* states,
    const int num_states
) {
    unsigned int i = (blockDim.x * blockIdx.x * m + threadIdx.x);
    unsigned int state_i = (blockDim.x * blockIdx.x + threadIdx.x) % num_states;
    size_t max_i = min(((size_t)i)+blockDim.x*m, n);
    rng_t state = states[state_i];
    for (unsigned int j=i; j<max_i; j+=blockDim.x) {
        result[j] = (scalar_t) (
            // curand_uniform produces floats x \in (0, 1]
            // use 1-x through offset and scale:
            // scale = vmax - vmin
            // offset = vmin + scale
            offset - scale * __curand_uniform<rng_t, temp_t>(&state)
        );
    }
    states[state_i] = state;
}


void RandomNumberGenerator::uniform(
        CudaTensor* target,
        double vmin,
        double vmax,
        unsigned int blocks_per_sm,
        unsigned int threads
) {
    //init_device_state();

    py::gil_scoped_release release;

    assert_contiguous(target);

    DLTensor &t = target->dl_tensor;

    if (t.ctx.device_id != device_id) {
        throw std::invalid_argument("tensor exceeds max size");
    }

    calc_threads(threads, device_id);
    size_t num;
    unsigned int num_blocks;
    unsigned int values_per_thread = 0;
    calc_blocks_values_1d(t, num_blocks, num, values_per_thread, threads, blocks_per_sm);

    if (num == 0) {
        return;
    }

    if (t.dtype.code == kDLInt || t.dtype.code == kDLUInt  ) {
        vmax += 1;
        if(t.dtype.bits <= 16){
            vmin *= 1+EPSILON_FLOAT;
            vmax *= 1-EPSILON_FLOAT;
        }
        else {
            vmin *= 1+EPSILON_DOUBLE;
            vmax *= 1-EPSILON_DOUBLE;
        }
    }
    double scale = vmax - vmin;
    double offset = vmin + scale;
    DISPATCH(t.dtype, "generate_uniform_kernel", ([&] {
        generate_uniform_kernel<rng_t, scalar_t, temp_t>
        <<<num_blocks, threads, 0, current_stream>>>(
            (scalar_t*) target->ptr(),
            num,
            values_per_thread,
            (temp_t) offset,
            (temp_t) scale,
            device_states,
            num_states
        );
    }));
    CUDA(cudaGetLastError());
    // mark tensors as in use
    target->record();
}


template<typename scalar_t>
__device__ __forceinline__ void __generate_normal2(
        scalar_t* result, unsigned int j, dim3 blockDim, rng_t* state,
        float mean, float std
) {
    float2 v = curand_normal2(state);
    saturate_cast<float, scalar_t>(std * v.x + mean, &result[j]);
    saturate_cast<float, scalar_t>(std * v.y + mean, &result[j+blockDim.x]);
}

template<typename scalar_t>
__device__ __forceinline__ void __generate_normal2(
        scalar_t* result, unsigned int j, dim3 blockDim, rng_t* state,
        double mean, double std
) {
    double2 v = curand_normal2_double(state);
    saturate_cast<double, scalar_t>(std * v.x + mean, &result[j]);
    saturate_cast<double, scalar_t>(std * v.y + mean, &result[j+blockDim.x]);
}

template<typename scalar_t>
__device__ __forceinline__ void __generate_normal(
        scalar_t* result, unsigned int j, rng_t* state,
        float mean, float std
) {
    saturate_cast<float, scalar_t>(std * curand_normal(state) + mean, &result[j]);
}

template<typename scalar_t>
__device__ __forceinline__ void __generate_normal(
        scalar_t* result, unsigned int j, rng_t* state,
        double mean, double std
) {
    saturate_cast<double, scalar_t>(std * curand_normal(state) + mean, &result[j]);
}


template<typename rng_t, typename scalar_t, typename temp_t>
__global__ void generate_gaussian_kernel(
    scalar_t* result,
    const ssize_t n,
    const unsigned int m,
    const temp_t mean,
    const temp_t std,
    rng_t* states,
    const unsigned int num_states
) {
    unsigned int i = (blockDim.x * blockIdx.x * m + threadIdx.x);
    size_t max_i = min(((size_t)i) + blockDim.x * m, n - blockDim.x);
    unsigned int state_i = (blockDim.x * blockIdx.x + threadIdx.x) % num_states;
    rng_t state = states[state_i];
    unsigned int j;
    for(j=i; j<max_i; j+=2*blockDim.x) {
        __generate_normal2<scalar_t>(result, j, blockDim, &state, mean, std);
    }
    if (j < n) {
        __generate_normal<scalar_t>(result, j, &state, mean, std);
    }
    states[state_i] = state;
}


void RandomNumberGenerator::gaussian(
        CudaTensor* target,
        double mean,
        double std,
        unsigned int blocks_per_sm,
        unsigned int threads
) {
    //init_device_state();

    py::gil_scoped_release release;

    assert_contiguous(target);

    DLTensor &t = target->dl_tensor;

    if (t.ctx.device_id != device_id) {
        throw std::invalid_argument("tensor must be on same device as generator");
    }

    calc_threads(threads, device_id);
    size_t num;
    unsigned int num_blocks;
    unsigned int values_per_thread = 0;
    calc_blocks_values_1d(t, num_blocks, num, values_per_thread, threads, blocks_per_sm);

    if (num == 0) {
        return;
    }

    DLDataType dtype = target->dl_tensor.dtype;
    DISPATCH(dtype, "generate_gaussian_kernel", ([&] {
        generate_gaussian_kernel<rng_t, scalar_t, temp_t>
        <<<num_blocks, threads, 0, current_stream>>>(
            (scalar_t*) target->ptr(),
            num,
            values_per_thread,
            (temp_t) mean,
            (temp_t) std,
            device_states,
            num_states
        ); })
    );
    CUDA(cudaGetLastError());
    // mark tensors as in use
    target->record();
}


// namespace augpy
}
