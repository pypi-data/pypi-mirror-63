#include <pybind11/stl.h>
#include <vector>
#include "cuda_runtime.h"
#include "nvjpeg.h"
#include "core.h"
#include "tensor.h"
#include "exception.h"
#include "nvjpegdecoder.h"


namespace augpy {


Decoder::Decoder(
        size_t devide_padding,
        size_t host_padding,
        bool gpu_huffman
){
    this->device_id = current_device;
    nvjpegBackend_t backend = NVJPEG_BACKEND_HYBRID;
    if (gpu_huffman) {
        backend = NVJPEG_BACKEND_GPU_HYBRID;
    }
    NVJPEG(nvjpegCreateEx(backend, NULL, NULL, 0, &handle));
    NVJPEG(nvjpegSetDeviceMemoryPadding(devide_padding, handle));
    NVJPEG(nvjpegSetPinnedMemoryPadding(host_padding, handle));
    NVJPEG(nvjpegJpegStateCreate(handle, &state));
    NVJPEG(nvjpegJpegStateCreate(handle, &state_batched));
}


Decoder::~Decoder(){
    nvjpegJpegStateDestroy(state_batched);
    nvjpegJpegStateDestroy(state);
    nvjpegDestroy(handle);
}


CudaTensor* Decoder::decode(std::string data, CudaTensor* buffer){
    const unsigned char* blob = (const unsigned char*) data.data();
    int nComponents;
    nvjpegChromaSubsampling_t subsampling;
    int widths[NVJPEG_MAX_COMPONENT];
    int heights[NVJPEG_MAX_COMPONENT];

    NVJPEG(nvjpegGetImageInfo(
        handle, blob, data.length(),
        &nComponents, &subsampling, &widths[0], &heights[0]
    ));

    int h = heights[0];
    int w = widths[0];
    int64_t shape[3] = {h, w, 3};

    CudaTensor* retval = NULL;
    if (!buffer) {
        buffer = retval = new CudaTensor(&shape[0], 3, dldtype_uint8, device_id);
    }

    check_tensor(buffer, h * w * 3);

    NVJPEG(nvjpegDecodePhaseOne(
        handle, state, blob, data.length(),
        NVJPEG_OUTPUT_RGBI, current_stream
    ));

    unsigned char* image = (unsigned char*) buffer->ptr();

    nvjpegImage_t destination;
    for(int i=1; i<NVJPEG_MAX_COMPONENT; i++) {
        destination.channel[i] = 0;
        destination.pitch[i] = 0;
    }
    destination.channel[0] = image;
    destination.pitch[0] = 3 * w;

    py::gil_scoped_acquire acquire;

    NVJPEG(nvjpegDecodePhaseTwo(handle, state, current_stream));
    NVJPEG(nvjpegDecodePhaseThree(handle, state, &destination, current_stream));

    // mark tensors as in use
    buffer->record();

    if (!retval) {
        retval = new CudaTensor(buffer, 3, &shape[0]);
    }
    return retval;
}


// namespace augpy
}
