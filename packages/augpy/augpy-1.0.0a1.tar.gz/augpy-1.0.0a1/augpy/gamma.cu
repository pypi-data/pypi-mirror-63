#include <cuda.h>
#include <cuda_runtime.h>
#include <vector>
#include "core.h"
#include "tensor.h"
#include "gamma.h"
#include "dispatch.h"


namespace augpy {


__device__ __forceinline__ float get_contrast_lookup(float a, float b, float w){
    float lut = 1 / (1 + expf(a+w*(b-a)));
    float max = 0.9981282f;
    float min = 0.0018718f;
    return (lut-min)/(max-min);
}

__device__ __forceinline__ float get_contrast_lookup_negative(float a, float b, float w){
    float lut = 2 * atanh(2 * (a+w*(b-a)) - 1);
    float max = 5.69603851f;
    float min = -5.69603851f;
    return (lut-min)/(max-min);
}


template <typename scalar_t, typename temp_t>
__global__ void gamma_kernel(
        scalar_t* src,
        scalar_t* dst,
        const float* const gamma_grays,
        const float* const gamma_colors,
        const float* const contrasts,
        const size_t N,
        const size_t C,
        const size_t count,
        const temp_t max_value,
        const unsigned int values_per_thread
){
    // contrast and gray gamma for current image
    const float contrast = contrasts[blockIdx.x];
    const float gray = gamma_grays[blockIdx.x];
    const temp_t one_by = 1/(temp_t)max_value;
    // first pixel in current image for this thread
    size_t idx = blockIdx.y * blockDim.x * values_per_thread + threadIdx.x;
    size_t last_idx = min(idx + blockDim.x * values_per_thread, C*count);
    // advanced src and dst to first pixel in image
    src += blockIdx.x * C * count;
    dst += blockIdx.x * C * count;
    // C is not a valid channel index,
    // so this will trigger loading of gamma_colors value
    size_t last_c = C;
    float gamma_color;
    for( ; idx<last_idx; idx+=blockDim.x){
        size_t c = idx / count;
        if (c != last_c) {
            gamma_color = gamma_colors[C*blockIdx.x+c];
        }
        last_c = c;
        scalar_t color = src[idx];
        temp_t fraction = (temp_t)color * one_by;
        temp_t baselookup = fraction;
        temp_t contrastlookup = 0;
        temp_t base = 0;
        if(contrast < 0){
            contrastlookup = get_contrast_lookup_negative(3.348e-03f, 1-3.348e-03f, fraction);
            base = (1+contrast)*baselookup - contrast*contrastlookup;
        }
        else{
            contrastlookup = get_contrast_lookup(6.279f, -6.279f, fraction);
            base = (1-contrast)*baselookup + contrast*contrastlookup;
        }
        dst[idx] = powf(base, gray*gamma_color)*max_value;
    }
}


template<typename scalar_t, typename temp_t, unsigned short VALUE_LIMIT, unsigned char MAX_CHANNELS>
__global__ void gamma_kernel_lut(
        scalar_t* src,
        scalar_t* dst,
        const float* gamma_grays,
        const float* gamma_colors,
        const float* contrasts,
        const size_t C,
        const size_t count,
        const scalar_t max_value,
        const unsigned int values_per_thread
){
    // contrast and gray gamma for current image
    const float gray = gamma_grays[blockIdx.x];
    const float contrast = contrasts[blockIdx.x];
    const temp_t one_by = (temp_t)1.0 / (temp_t)max_value;
    // prepare lookup table in shared memory
    __shared__ scalar_t lut[VALUE_LIMIT*MAX_CHANNELS];
    for (size_t c=0; c<C; ++c) {
        float gamma_color = gamma_colors[C * blockIdx.x + c];
        unsigned short lidx = threadIdx.x;
        for ( ; lidx<=max_value; lidx+=blockDim.x) {
            temp_t fraction = (temp_t)lidx * one_by;
            if(contrast < 0){
                fraction = (1 + contrast) * fraction
                         - contrast * get_contrast_lookup_negative(3.348e-03, 1-3.348e-03, fraction);
            }
            else{
                fraction = (1 - contrast) * fraction
                         + contrast * get_contrast_lookup(6.279, -6.279, fraction);
            }
            lut[c*VALUE_LIMIT+lidx] = powf(fraction, gray * gamma_color) * max_value;
        }
    }

    __syncthreads();

    // first pixel in current image for this thread
    size_t idx = blockIdx.y * blockDim.x * values_per_thread + threadIdx.x;
    size_t last_idx = min(idx + blockDim.x * values_per_thread, C*count);
    // advance src to first pixel for this thread
    src += blockIdx.x * C * count;
    dst += blockIdx.x * C * count;
    // loop until last index
    for( ; idx<last_idx; idx+=blockDim.x){
        dst[idx] = lut[VALUE_LIMIT * (idx / count) + min(src[idx], max_value)];
    }
}


CudaTensor* add_gamma(
    CudaTensor* imtensor,
    CudaTensor* gammagrays,
    CudaTensor* gammacolors,
    CudaTensor* contrasts,
    double max_value,
    CudaTensor* out
){
    assert_contiguous(imtensor);
    assert_contiguous(gammagrays);
    assert_contiguous(gammacolors);
    assert_contiguous(contrasts);

    CudaTensor* retval = NULL;
    if (!out) {
        out = retval = empty_like(imtensor);
    }

	DLTensor &im_tensor = imtensor->dl_tensor;
    int64_t N = im_tensor.shape[0];
    int64_t C = im_tensor.shape[1];
    int64_t H = im_tensor.shape[2];
    int64_t W = im_tensor.shape[3];

    check_same_dtype_device(im_tensor, out->dl_tensor);

    unsigned int num_threads = 0;
    calc_threads(num_threads, im_tensor.ctx.device_id);
    cudaDeviceProp props = get_device_properties(im_tensor.ctx.device_id);
    unsigned int blocks_per_sm = 8;
    unsigned int num_blocks = ceil_div(props.multiProcessorCount * blocks_per_sm, N);
    int64_t count = H*W;
    int64_t vpt = ceil_div(C*count, num_blocks * num_threads);
    unsigned int values_per_thread = min(
        (int64_t)std::numeric_limits<unsigned int>().max(),
        vpt
    );
    num_blocks = ceil_div(ceil_div(C*count, values_per_thread), num_threads);
    dim3 grid(N, num_blocks);

    if(im_tensor.dtype.code == kDLUInt && im_tensor.dtype.bits == 8 && C <= 4 && max_value <= 256){
        gamma_kernel_lut<unsigned char, float, 256, 4>
        <<<grid, num_threads, 256*4, current_stream>>>(
            (unsigned char*)imtensor->ptr(),
            (unsigned char*)out->ptr(),
            (float*)gammagrays->ptr(),
            (float*)gammacolors->ptr(),
            (float*)contrasts->ptr(),
            C, count, (unsigned char)max_value, values_per_thread
        );
    }
    else{
        DISPATCH(im_tensor.dtype, "add_gamma_kernel_dynamic", ([&] {
            gamma_kernel<scalar_t, temp_t>
            <<<grid, num_threads, 0, current_stream>>>(
                (scalar_t*)imtensor->ptr(),
                (scalar_t*)out->ptr(),
                (float*)gammagrays->ptr(),
                (float*)gammacolors->ptr(),
                (float*)contrasts->ptr(),
                N, C, count, (temp_t)max_value, values_per_thread
            );
        }));
    }

    CUDA(cudaGetLastError());

    // mark tensors as in use
    imtensor->record();
    gammagrays->record();
    gammacolors->record();
    contrasts->record();
    out->record();

    return retval;
}


// namespace augpy
}
