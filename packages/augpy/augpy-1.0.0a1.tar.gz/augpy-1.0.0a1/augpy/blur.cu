#include <pybind11/pybind11.h>
#include <cuda.h>
#include <cuda_runtime.h>
#include "core.h"
#include "tensor.h"
#include "saturate_cast.cuh"
#include "blur.h"
#include "dispatch.h"
#include "exception.h"


namespace augpy {


#define clamp(x,a,b) min(max(x,a),b)
#define BLOCKSIZE 16
#define MAX_SMEM_PER_BLOCK 48*1024
#define SQRT_TWO_PI 2.50662827463
#define SQRT_TWO 1.41421356237


template <typename scalar_t, typename temp_t>
__global__ void box_blur_single_kernel(
        scalar_t* image,
        scalar_t* target,
        const int ksize,
        const int offset,
        const temp_t norm,
        const int C,
        const int H,
        const int W,
        const ssize_t image_channel_stride,
        const ssize_t target_channel_stride
) {
    extern __shared__ char smem[];

    const int source_x = blockIdx.y * blockDim.x + threadIdx.x;
    const int source_y = blockIdx.z * blockDim.y + threadIdx.y;

    target += source_y*W + source_x;

    const int shared_w = blockDim.x + ksize - 1;
    const int shared_h = blockDim.y + ksize - 1;
    temp_t* horizontal_data = reinterpret_cast<temp_t*>(smem);
    temp_t* vertical_data = &horizontal_data[shared_h * shared_w];
    const int first_i = threadIdx.y * blockDim.x + threadIdx.x;
    const int num_threads = blockDim.x * blockDim.y;

    const int maxx = W-1;
    const int maxy = H-1;
    const int offset_x = (int)(blockIdx.y * blockDim.x) - offset;
    const int offset_y = (int)(blockIdx.z * blockDim.y) - offset;
    for(int c=0; c<C; c++){
        for(int i=first_i; i<shared_h*shared_w ; i+=num_threads){
            int x = clamp(i % shared_w + offset_x, 0, maxx);
            int y = clamp(i / shared_w + offset_y, 0, maxy);
            horizontal_data[i] = image[y*W + x];
        }

        __syncthreads();

        for(int i=first_i; i<shared_h*blockDim.x; i+=num_threads) {
            int x = i % blockDim.x;
            int y = i / blockDim.x;
            temp_t sum = 0;
            for(int k=0; k<ksize; k++) {
                sum += horizontal_data[y*shared_w + x + k];
            }
            vertical_data[i] = sum * norm;
        }

        __syncthreads();

        if(source_x >= W || source_y >= H){
            image += image_channel_stride;
            target += target_channel_stride;
            continue;
        }

        temp_t sum = 0;
        for(int k=0; k<ksize; k++) {
            sum += vertical_data[(threadIdx.y + k) * blockDim.x + threadIdx.x];
        }
        saturate_cast<temp_t, scalar_t>(sum * norm, target);
        image += image_channel_stride;
        target += target_channel_stride;
    }
}


CudaTensor* box_blur_single(
        CudaTensor* input,
        int ksize,
        CudaTensor* out
) {
    CudaTensor* retval = NULL;
    if (!out) {
        out = retval = empty_like(input);
    }

    assert_contiguous(input);
    assert_contiguous(out);

    DLTensor &input_tensor = input->dl_tensor;
    DLTensor &out_tensor = out->dl_tensor;

    if(input_tensor.ndim != 3 || out_tensor.ndim != 3) {
        throw std::invalid_argument("need 3D input and output tensors");
    }

    int C = input_tensor.shape[0];
    int H = input_tensor.shape[1];
    int W = input_tensor.shape[2];

    if(!array_equals(0, 3, input_tensor.shape, out_tensor.shape)) {
        throw std::invalid_argument("input and output shapes need to be equal");
    }

    const int shared_size = BLOCKSIZE + ksize - 1;
    int shared_memory;
    dim3 grid_dim(1, (W+BLOCKSIZE-1)/BLOCKSIZE, (H+BLOCKSIZE-1)/BLOCKSIZE);
    dim3 block_dim(BLOCKSIZE, BLOCKSIZE, 1);

    DISPATCH(input_tensor.dtype, "box_blur_single_kernel", ([&] {
        shared_memory = ksize * sizeof(temp_t)
                      + shared_size * shared_size * sizeof(temp_t)
                      + BLOCKSIZE * shared_size * sizeof(temp_t);

        if(shared_memory > MAX_SMEM_PER_BLOCK) {
            throw std::invalid_argument("kernel size too large.");
        }
        box_blur_single_kernel<scalar_t, temp_t>
        <<<grid_dim, block_dim, shared_memory, current_stream>>>(
            (scalar_t*)input->ptr(),
            (scalar_t*)out->ptr(),
            ksize,
            ksize / 2,
            1.F / (float) ksize,
            C, H, W, H*W, H*W
        );
    }));
    CUDA(cudaGetLastError());
    input->record();
    out->record();

    return retval;
}


template <typename temp_t>
__device__ __forceinline__ void create_gaussian_kernel(
        temp_t* kernel,
        float sigma,
        int ksize,
        int range
) {
    if(threadIdx.y * blockDim.x + threadIdx.x < range+1){
        int k = threadIdx.y * blockDim.x + threadIdx.x;
        kernel[k] = exp(-(temp_t)(k * k) / (2 * sigma * sigma));
        temp_t scale = kernel[0];
        for(int s=1; s<range+1; s++) {
            scale += 2 * kernel[s];
        }
        kernel[k] /= scale;
    }
}


template <typename scalar_t, typename temp_t>
__device__ __forceinline__ void gaussian_blur_separable(
        scalar_t* image,
        scalar_t* target,
        temp_t* kernel,
        const int ksize,
        const int range,
        const int source_x,
        const int source_y,
        const int C,
        const int H,
        const int W,
        const ssize_t image_channel_stride,
        const ssize_t target_channel_stride
) {
    const int shared_w = blockDim.x + ksize - 1;
    const int shared_h = blockDim.y + ksize - 1;
    temp_t* horizontal_data = &kernel[range+1];
    temp_t* vertical_data = &horizontal_data[shared_h * shared_w];
    const int first_i = threadIdx.y * blockDim.x + threadIdx.x;
    const int num_threads = blockDim.x * blockDim.y;
    const int maxx = W-1;
    const int maxy = H-1;
    const int offset_x = (int)(blockIdx.y * blockDim.x) - range;
    const int offset_y = (int)(blockIdx.z * blockDim.y) - range;

    for(int c=0; c<C; c++){
        for(int i=first_i; i<shared_h*shared_w ; i+=num_threads){
            int x = clamp(i % shared_w + offset_x, 0, maxx);
            int y = clamp(i / shared_w + offset_y, 0, maxy);
            horizontal_data[i] = image[y*W + x];
        }

        __syncthreads();

        for(int i=first_i; i<shared_h*blockDim.x; i+=num_threads) {
            int x = i % blockDim.x;
            int y = i / blockDim.x;
            temp_t sum = 0;
            for(int k=0; k<ksize; k++) {
                sum += kernel[abs(k-range)] * horizontal_data[y*shared_w + x + k];
            }
            vertical_data[i] = sum;
        }

        __syncthreads();

        if(source_x >= W || source_y >= H){
            image += image_channel_stride;
            target += target_channel_stride;
            continue;
        }

        temp_t sum = 0;
        for(int k=0; k<ksize; k++) {
            sum += kernel[abs(k-range)] * vertical_data[(threadIdx.y + k) * blockDim.x + threadIdx.x];
        }
        
        saturate_cast<temp_t, scalar_t>(sum, target);

        image += image_channel_stride;
        target += target_channel_stride;
    }
}


template <typename scalar_t, typename temp_t>
__global__ void gaussian_blur_kernel(
        scalar_t* image,
        scalar_t* target,
        const float* sigmas,
        const int max_ksize,
        const int C,
        const int H,
        const int W,
        const ssize_t image_image_stride,
        const ssize_t image_channel_stride,
        const ssize_t target_image_stride,
        const ssize_t target_channel_stride
) {
    extern __shared__ char smem[];
    temp_t* kernel = reinterpret_cast<temp_t*>(smem);
    const int source_x = blockIdx.y * blockDim.x + threadIdx.x;
    const int source_y = blockIdx.z * blockDim.y + threadIdx.y;

    image += blockIdx.x * image_image_stride;
    target += blockIdx.x * target_image_stride + source_y*W + source_x;

    const float sigma = sigmas[blockIdx.x];
    int ksize = (int)(sigma * 6.6f - 2.3f);
    // required kernel size is <= 1, so blur would have no effect
    if(ksize <= 1) {
        if(source_x >= W || source_y >= H) {
            return;
        }
        image += source_y*W + source_x;
        for (int c=0; c<C; c++) {
            *target = *image;
            image += image_channel_stride;
            target += target_channel_stride;
        } 
        return;
    }
    ksize = min(max_ksize, max(3, ksize | 1));
    const int range = ksize / 2;

    create_gaussian_kernel(kernel, sigma, ksize, range);
    gaussian_blur_separable(
        image, target, kernel, ksize, range, source_x, source_y, C, H, W,
        image_channel_stride, target_channel_stride
    );
}


CudaTensor* gaussian_blur(
        CudaTensor* input,
        CudaTensor* sigmas,
        int max_ksize,
        CudaTensor* out
) {
    CudaTensor* retval = NULL;
    if (!out) {
        out = retval = empty_like(input);
    }

    assert_contiguous(input);
    assert_contiguous(sigmas);
    assert_contiguous(out);

    DLTensor &input_tensor = input->dl_tensor;   
    DLTensor &out_tensor = out->dl_tensor;
    DLTensor &sigmas_tensor = sigmas->dl_tensor;

    if(sigmas_tensor.dtype.code != kDLFloat || sigmas_tensor.dtype.bits != 32) {
        throw std::invalid_argument("sigmas must be float32");
    }

    if(input_tensor.ndim != 4 || out_tensor.ndim != 4) {
        throw std::invalid_argument("need 4D input and output tensors");
    }

    int N = input_tensor.shape[0];
    int C = input_tensor.shape[1];
    int H = input_tensor.shape[2];
    int W = input_tensor.shape[3];

    if(!array_equals(0, 4, input_tensor.shape, out_tensor.shape)) {
        throw std::invalid_argument("input and output shapes need to be equal");
    }

    max_ksize = max(3, max_ksize | 1);
    const int shared_size = BLOCKSIZE + max_ksize - 1;
    int shared_memory;
    dim3 grid_dim(N, (W+BLOCKSIZE-1)/BLOCKSIZE, (H+BLOCKSIZE-1)/BLOCKSIZE);
    dim3 block_dim(BLOCKSIZE, BLOCKSIZE, 1);

    DISPATCH(input_tensor.dtype, "gaussian_blur_kernel", ([&] {
        shared_memory = (max_ksize + shared_size * shared_size
                         + BLOCKSIZE * shared_size) * sizeof(temp_t);
        if(shared_memory > MAX_SMEM_PER_BLOCK) {
            throw std::invalid_argument("sigma must be <= 30");
        }
        gaussian_blur_kernel<scalar_t, temp_t>
        <<<grid_dim, block_dim, shared_memory, current_stream>>>(
            (scalar_t*)input->ptr(),
            (scalar_t*)out->ptr(),
            (float*)sigmas->ptr(), max_ksize,
            C, H, W, C*H*W, H*W, C*H*W, H*W
        );
    }));
    CUDA(cudaGetLastError());

    input->record();
    sigmas->record();
    out->record();

    return retval;
}


template <typename scalar_t, typename temp_t>
__global__ void gaussian_blur_single_kernel(
        scalar_t* image,
        scalar_t* target,
        const float sigma,
        const int ksize,
        const int range,
        const int C,
        const int H,
        const int W,
        const ssize_t image_channel_stride,
        const ssize_t target_channel_stride
) {
    extern __shared__ char smem[];
    temp_t* kernel = reinterpret_cast<temp_t*>(smem);

    const int source_x = blockIdx.y * blockDim.x + threadIdx.x;
    const int source_y = blockIdx.z * blockDim.y + threadIdx.y;
    target += source_y*W + source_x;

    create_gaussian_kernel(kernel, sigma, ksize, range);
    gaussian_blur_separable(
        image, target, kernel, ksize, range, source_x, source_y, C, H, W,
        image_channel_stride, target_channel_stride
    );
}


CudaTensor* gaussian_blur_single(
        CudaTensor* input,
        float sigma,
        CudaTensor* out
) {
    CudaTensor* retval = NULL;
    if (!out) {
        out = retval = empty_like(input);
    }

    assert_contiguous(input);
    assert_contiguous(out);

    DLTensor &input_tensor = input->dl_tensor;
    DLTensor &out_tensor = out->dl_tensor;

    if(input_tensor.ndim != 3 || out_tensor.ndim != 3) {
        throw std::invalid_argument("need 3D input and output tensors");
    }

    int C = input_tensor.shape[0];
    int H = input_tensor.shape[1];
    int W = input_tensor.shape[2];

    if(!array_equals(0, 3, input_tensor.shape, out_tensor.shape)) {
        throw std::invalid_argument("input and output shapes need to be equal");
    }

    int ksize = (int)(sigma * 6.6f - 2.3f);
    // required kernel size is <= 1, so blur would have no effect
    if(ksize <= 1) {
        copy(input, out);
    }
    else {
        ksize = max(3, ksize | 1);
        const int shared_size = BLOCKSIZE + ksize - 1;
        int shared_memory;
        dim3 grid_dim(1, (W+BLOCKSIZE-1)/BLOCKSIZE, (H+BLOCKSIZE-1)/BLOCKSIZE);
        dim3 block_dim(BLOCKSIZE, BLOCKSIZE, 1);
        DISPATCH(input_tensor.dtype, "gaussian_blur_single_kernel", ([&] {
            shared_memory = (ksize/2+1) * sizeof(temp_t)
                          + shared_size * shared_size * sizeof(temp_t)
                          + BLOCKSIZE * shared_size * sizeof(temp_t);

            if(shared_memory > MAX_SMEM_PER_BLOCK) {
                throw std::invalid_argument("sigma must be <= 30");
            }
            gaussian_blur_single_kernel<scalar_t, temp_t>
            <<<grid_dim, block_dim, shared_memory, current_stream>>>(
                (scalar_t*)input->ptr(),
                (scalar_t*)out->ptr(),
                sigma, ksize, ksize/2, C, H, W, H*W, H*W
            );
        }));
        CUDA(cudaGetLastError());
        // mark tensors as in use
        input->record();
        out->record();
    }

    return retval;
}


// namespace augpy
}
