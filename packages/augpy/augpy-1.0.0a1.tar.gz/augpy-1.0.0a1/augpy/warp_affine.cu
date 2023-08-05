#include "warp_affine.h"
#include "cuda_runtime.h"
#include "saturate_cast.cuh"
#include "exception.h"
#include "core.h"
#include "tensor.h"
#include "dispatch.h"
#include <iostream>


#ifndef _USE_MATH_DEFINES
#define _USE_MATH_DEFINES
#endif
#include <math.h>


namespace py = pybind11;


namespace augpy {


#define MAX_THREADS 128
#define CHANNEL_BLOCK_SIZE 3
#define deg2rad(angle) angle*M_PI/180
#define MAX_SUPERSAMPLING 3
#define BLOCK_SIZE 16


int make_affine_matrix(
        py::buffer out,
        size_t source_height,
        size_t source_width,
        size_t target_height,
        size_t target_width,
        float angle,
        float scale,
        float aspect,
        float shifty,
        float shiftx,
        float sheary,
        float shearx,
        bool hmirror,
        bool vmirror,
        WarpScaleMode scale_mode,
        int max_supersampling
) {
    if (scale == 0) {
        throw std::invalid_argument("scale must be != 0");
    }
    if (aspect == 0) {
        throw std::invalid_argument("aspect must be != 0");
    }

    py::buffer_info out_info = out.request();
    py::gil_scoped_release release;

    if (!check_contiguous(out_info)) {
        throw std::invalid_argument("need contiguous matrix");
    }
    if (out_info.ndim != 2 || out_info.shape[0] < 2 || out_info.shape[1]!=3) {
        throw std::invalid_argument("need 2x3 matrix");
    }
    if (out_info.format.compare("f") != 0) {
        throw std::invalid_argument("matrix must be float32");
    }

    float* outp = (float*) out_info.ptr;

    double sw = (double)source_width / 2.0;
    double sh = (double)source_height / 2.0;
    double tw = (double)target_width / 2.0;
    double th = (double)target_height / 2.0;

    double r;
    if (scale_mode == WARP_SCALE_LONGEST)
        r = max(sh / th, sw / tw) / scale;
    else if (scale_mode == WARP_SCALE_SHORTEST)
        r = min(sh / th, sw / tw) / scale;
    else
        throw std::invalid_argument("unknown scale mode");

    double wdelta = max(sw - tw*r, tw*r - sw);
    double hdelta = max(sh - th*r, th*r - sh);

    double rad = deg2rad(-angle);
    double cos_rad = cos(rad);
    double sin_rad = sin(rad);

    double p1 = -tw - shearx * th;
    double p2 = -tw * sheary - th;
    double p3 = r * aspect * (hmirror ? -1 : 1);
    double p4 = r / aspect * (vmirror ? -1 : 1);

    outp[0] = cos_rad * p3 + sin_rad * p4 * sheary;
    outp[1] = cos_rad * p3 * shearx + sin_rad * p4;
    outp[2] = cos_rad * p3 * p1 + sin_rad * p4 * p2
            + sw + wdelta * shiftx;

    outp[3] = cos_rad * p4 * sheary - sin_rad * p3;
    outp[4] = cos_rad * p4 - sin_rad * p3 * shearx;
    outp[5] = cos_rad * p4 * p2 - sin_rad * p3 * p1
            + sh + hdelta * shifty;

    int supersampling = max(1, min(max_supersampling, (int) ceil(r)));
    return supersampling;
}


#define warp(x,y,xnew,ynew,m0,m1,m2,m3,m4,m5) { \
    xnew = m0*x+m1*y+m2; \
    ynew = m3*x+m4*y+m5; \
}
#define index_hwc(x,y,c,src_W,src_C) \
    (size_t)(y)*src_W*src_C + (size_t)(x)*src_C + c
#define index_chw(x,y,c,src_H,src_W) \
    c*src_H*src_W + (size_t)(y)*src_W + (size_t)(x)
#define check_index(v, vmax) \
    v>=0 && v<vmax
#define check_floor(v, vmax) \
    v>=0 && v<vmax
#define check_ceil(v, vmax) \
    v>-1 && v<=vmax-1
#define interpolate(x, y, ul, ur, dl, dr) \
    y * (x*ur + (1-x)*ul) + (1-y)*(x*dr + (1-x)*dl)


template <typename scalar_t, typename temp_t>
__global__ void warp_kernel(
        const scalar_t* const src,
        const int src_H, const int src_W, const int src_C,
        scalar_t* dst,
        const int dst_C, const int dst_H, const int dst_W,
        const scalar_t* const background,
        const float m0,
        const float m1,
        const float m2,
        const float m3,
        const float m4,
        const float m5,
        const float offset,
        const float step,
        const temp_t norm
){
    const int block = blockIdx.x;
    const int id = blockIdx.y * blockDim.x + threadIdx.x;
    const int idx = id % dst_W;
    const int idy = id / dst_W;
    const int first_channel = block * CHANNEL_BLOCK_SIZE;
    const int last_channel = min(first_channel+CHANNEL_BLOCK_SIZE, src_C);
    const int n_channels = last_channel - first_channel;
    if(id >= dst_H*dst_W) return;
    temp_t color[CHANNEL_BLOCK_SIZE];
    for(int i=0; i<n_channels; i++){
        color[i]=0;
    }
    temp_t bg[CHANNEL_BLOCK_SIZE];
    for(int c=0; c<n_channels; c++){
        bg[c] = background[c+first_channel];
    }
    float ymin = (float)idy - offset;
    float ymax = (float)idy + offset + 1e-5f;
    float xmin = (float)idx - offset;
    float xmax = (float)idx + offset + 1e-5f;
    for(float posy=ymin; posy<ymax; posy+=step){
        for(float posx=xmin; posx<xmax; posx+=step){
            float newx, newy;
            warp(posx, posy, newx, newy, m0, m1, m2, m3, m4, m5);
            float floor_x = floor(newx);
            float floor_y = floor(newy);
            float ceil_x = ceil(newx);
            float ceil_y = ceil(newy);
            float rx = newx - floor_x;
            float ry = ceil_y - newy;
            bool floor_x_ok = check_index(floor_x, src_W);
            bool floor_y_ok = check_index(floor_y, src_H);
            bool ceil_x_ok = check_index(ceil_x, src_W);
            bool ceil_y_ok = check_index(ceil_y, src_H);
            for(int c=first_channel; c<last_channel; c++){
                temp_t back = bg[c-first_channel];
                float ul = floor_x_ok && floor_y_ok ?
                    src[index_hwc(floor_x,floor_y,c,src_W,src_C)] : back;
                float dl = floor_x_ok && ceil_y_ok ?
                    src[index_hwc(floor_x,ceil_y,c,src_W,src_C)] : back;
                float ur = ceil_x_ok && floor_y_ok ?
                    src[index_hwc(ceil_x,floor_y,c,src_W,src_C)] : back;
                float dr = ceil_x_ok && ceil_y_ok ?
                    src[index_hwc(ceil_x,ceil_y,c,src_W,src_C)] : back;
                color[c-first_channel] += interpolate(rx, ry, ul, ur, dl, dr);
            }
        }
    }
    for(size_t c=first_channel; c<last_channel; c++){
        saturate_cast<temp_t, scalar_t>(
            color[c-first_channel] * norm,
            &dst[index_chw(idx,idy,c,dst_H,dst_W)]
        );
    }
}


void warp_affine(
        CudaTensor* src,
        CudaTensor* dst,
        py::buffer matrix,
        CudaTensor* background,
        int supersampling
){
    py::buffer_info matrix_info = matrix.request();

    py::gil_scoped_release release;

    check_tensor(src);
    check_tensor(dst);
    check_tensor(background);

    DLTensor& st = src->dl_tensor;
    DLTensor& dt = dst->dl_tensor;
    DLTensor& bt = background->dl_tensor;

    if (st.ndim != 3 || dt.ndim != 3) {
        throw std::invalid_argument("need 3D DLTensors for src and dst");
    }
    if (st.shape[2] != dt.shape[0]) {
        throw std::invalid_argument("src shape[2] and dst shape[0] must match");
    }
    if (!check_contiguous(matrix_info)) {
        throw std::invalid_argument("need contiguous matrix");
    }
    if (matrix_info.ndim != 2 || matrix_info.shape[0] < 2 || matrix_info.shape[1]!=3){
        throw std::invalid_argument("need 2x3 matrix");
    }
    if (matrix_info.format.compare("f") != 0) {
        throw std::invalid_argument("matrix must be float32");
    }
    if (bt.shape[0] != dt.shape[0]) {
        throw std::invalid_argument("background must match channels");
    }

    const float* matrixp = (const float*) matrix_info.ptr;
    const size_t channel_blocks = ceil_div(dt.shape[0], CHANNEL_BLOCK_SIZE);
    const float step = 1.0f / (float) supersampling;
    const float offset = (float)(supersampling - 1) * step / 2.0f;
    const double norm = 1.0 / (double)(supersampling*supersampling);
    int num_blocks = ceil_div(dt.shape[1] * dt.shape[2], MAX_THREADS);
    dim3 grid(channel_blocks, num_blocks, 1);

    DISPATCH(st.dtype, "warp_kernel", ([&] {
        warp_kernel<scalar_t, temp_t>
        <<<grid, MAX_THREADS, 0, current_stream>>>(
                (const scalar_t*) src->ptr(),
                st.shape[0], st.shape[1], st.shape[2],
                (scalar_t*) dst->ptr(),
                dt.shape[0], dt.shape[1], dt.shape[2],
                (const scalar_t*) background->ptr(),
                matrixp[0],
                matrixp[1],
                matrixp[2],
                matrixp[3],
                matrixp[4],
                matrixp[5],
                offset,
                step,
                norm
        ); })
    );

    CUDA(cudaGetLastError());
    // mark tensors as in use
    src->record();
    dst->record();
    background->record();
}


// namespace augpy
}
