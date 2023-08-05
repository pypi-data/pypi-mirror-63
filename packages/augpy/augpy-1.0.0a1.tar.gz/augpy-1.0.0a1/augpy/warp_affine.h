#ifndef AUGPY_WARP_AFFINE_H
#define AUGPY_WARP_AFFINE_H


#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <vector>
#include "tensor.h"


namespace py = pybind11;


namespace augpy {


enum WarpScaleMode {
    WARP_SCALE_SHORTEST,
    WARP_SCALE_LONGEST
};


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
);


void warp_affine(
        CudaTensor* src,
        CudaTensor* dst,
        py::buffer matrix,
        CudaTensor* background,
        int supersampling
);


// namespace augpy
}


// AUGPY_WARP_AFFINE_H
#endif
