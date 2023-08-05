#ifndef AUGPY_NVJPEGDECODER_H
#define AUGPY_NVJPEGDECODER_H


#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "nvjpeg.h"
#include "tensor.h"


namespace py = pybind11;


namespace augpy {


class Decoder {
public:
    Decoder(
        size_t devide_padding,
        size_t host_padding,
        bool gpu_huffman
    );

    ~Decoder();

    CudaTensor* decode(std::string data, CudaTensor* buffer);

private:
    int device_id;
    nvjpegHandle_t handle;
    nvjpegJpegState_t state;
    nvjpegJpegState_t state_batched;
};


// namespace augpy
}


// AUGPY_NVJPEGDECODER_H
#endif
