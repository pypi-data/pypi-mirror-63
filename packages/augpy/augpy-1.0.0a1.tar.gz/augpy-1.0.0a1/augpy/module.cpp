#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "dlpack.h"
#include "core.h"
#include "tensor.h"
#include "function.h"
#include "exception.h"
#include "random.h"
#include "nvjpegdecoder.h"
#include "warp_affine.h"
#include "gamma.h"
#include "blur.h"
#include "reduce.h"
#include <tuple>



namespace py = pybind11;
using namespace augpy;


PYBIND11_MODULE(_augpy, m) {
    m.doc() = "Python bindings for image processing CUDA functions";

    py::class_<CudaEvent> cudaevent(m, "CudaEvent");
    cudaevent
        .def(py::init())
        .def("record", &CudaEvent::record)
        .def("query", &CudaEvent::query)
        .def("synchronize", &CudaEvent::synchronize,
            py::arg("microseconds")=100,
            py::call_guard<py::gil_scoped_release>()
        );

    py::class_<CudaStream> cudastream(m, "CudaStream");
    cudastream
        .def(
            py::init<int, int>(),
            py::arg("device_id")=0,
            py::arg("priority")=0
        )
        .def("activate", &CudaStream::activate)
        .def("deactivate", &CudaStream::deactivate)
        .def("synchronize", &CudaStream::synchronize,
            py::arg("microseconds")=100,
            py::call_guard<py::gil_scoped_release>()
        );

    m.attr("default_stream") = default_stream;

    m.def("release", &release);

    py::class_<cudaDevicePropEx> props(m, "CudaDeviceProp", py::module_local());
    props
        .def_readonly("name", &cudaDevicePropEx::name)
        .def_readonly("major", &cudaDevicePropEx::major)
        .def_readonly("minor", &cudaDevicePropEx::minor)
        .def_readonly("multiProcessorCount", &cudaDevicePropEx::multiProcessorCount)
        .def_property_readonly("coresPerMultiprocessor", [](cudaDevicePropEx props) {
            return cores_per_sm(props.major, props.minor);
        })
        .def_readonly("l2CacheSize", &cudaDevicePropEx::l2CacheSize)
        .def_property_readonly("maxGridSize", [](cudaDevicePropEx props) {
            py::tuple size = py::tuple(3);
            size[0] = props.maxGridSize[0];
            size[1] = props.maxGridSize[1];
            size[2] = props.maxGridSize[2];
            return size;
        })
        .def_readonly("maxThreadsDim", &cudaDevicePropEx::maxThreadsDim)
        .def_readonly("maxThreadsPerBlock", &cudaDevicePropEx::maxThreadsPerBlock)
        .def_readonly("maxThreadsPerMultiProcessor", &cudaDevicePropEx::maxThreadsPerMultiProcessor)
        .def_readonly("regsPerBlock", &cudaDevicePropEx::regsPerBlock)
        .def_readonly("regsPerMultiprocessor", &cudaDevicePropEx::regsPerMultiprocessor)
        .def_readonly("sharedMemPerBlock", &cudaDevicePropEx::sharedMemPerBlock)
        .def_readonly("sharedMemPerMultiprocessor", &cudaDevicePropEx::sharedMemPerMultiprocessor)
        .def_readonly("totalConstMem", &cudaDevicePropEx::totalConstMem)
        .def_readonly("totalGlobalMem", &cudaDevicePropEx::totalGlobalMem)
        .def_readonly("warpSize", &cudaDevicePropEx::warpSize)
        .def_readonly("streamPrioritiesSupported", &cudaDevicePropEx::streamPrioritiesSupported)
        .def_readonly("leastStreamPriority", &cudaDevicePropEx::leastStreamPriority)
        .def_readonly("greatestStreamPriority", &cudaDevicePropEx::greatestStreamPriority);

    m.def("get_device_properties", &get_device_properties);

    py::class_<DLDataType> dtype(m, "DLDataType");
    dtype
        .def(
            py::init<unsigned char, unsigned char, unsigned short>(),
            py::arg("code"),
            py::arg("bits"),
            py::arg("lanes")=1
        )
        .def_readonly("code", &DLDataType::code)
        .def_readonly("bits", &DLDataType::bits)
        .def_readonly("lanes", &DLDataType::lanes)
        .def_property_readonly("itemsize", [](DLDataType self) {
            return itemsize(self);
        })
        .def("__repr__", &dldatatype_repr);

    py::enum_<DLDataTypeCode>(m, "DLDataTypeCode")
        .value("kDLInt", DLDataTypeCode::kDLInt)
        .value("kDLUInt", DLDataTypeCode::kDLUInt)
        .value("kDLFloat", DLDataTypeCode::kDLFloat)
        .export_values();

    m.attr("int8") = dldtype_int8;
    m.attr("uint8") = dldtype_uint8;
    m.attr("int16") = dldtype_int16;
    m.attr("uint16") = dldtype_uint16;
    m.attr("int32") = dldtype_int32;
    m.attr("uint32") = dldtype_uint32;
    m.attr("int64") = dldtype_int64;
    m.attr("uint64") = dldtype_uint64;
    m.attr("float16") = dldtype_float16;
    m.attr("float32") = dldtype_float32;
    m.attr("float64") = dldtype_float64;

    py::class_<CudaTensor> cudatensor(m, "CudaTensor");
    cudatensor
        .def(
            py::init<std::vector<ssize_t>, DLDataType, int>(),
            py::arg("shape"),
            py::arg("dtype")=dldtype_uint8,
            py::arg("device_id")=0,
            py::return_value_policy::take_ownership
        )
        .def("__add__", &add_scalar,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__add__", &add_tensor,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__radd__", &add_scalar,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__sub__", &sub_scalar,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__sub__", &sub_tensor,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__rsub__", &rsub_scalar,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__mul__", &mul_scalar,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__mul__", &mul_tensor,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__rmul__", &mul_scalar,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__truediv__", &div_scalar,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__truediv__", &div_tensor,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__rtruediv__", &rdiv_scalar,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__lt__", &lt_scalar,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__lt__", &lt_tensor,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__le__", &le_tensor,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__le__", &le_scalar,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__gt__", &gt_scalar,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__gt__", [](CudaTensor* self, CudaTensor* other, CudaTensor* out,
                          int blocks_per_sm, int threads) {
                return le_tensor(other, self, out, blocks_per_sm, threads);
            },
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__ge__", &ge_scalar,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__ge__", [](CudaTensor* self, CudaTensor* other, CudaTensor* out,
                          int blocks_per_sm, int threads) {
                return lt_tensor(other, self, out, blocks_per_sm, threads);
            },
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__eq__", &eq_scalar,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        .def("__eq__", &eq_tensor,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("scalar"),
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=512
        )
        // TODO add inplace __i*__ methods
        .def("__repr__", &CudaTensor::repr,
            py::return_value_policy::take_ownership)
        .def("__getitem__", &CudaTensor::index,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::keep_alive<0, 1>())
        .def("__getitem__", &CudaTensor::slice_simple,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::keep_alive<0, 1>())
        .def("__getitem__", &CudaTensor::slice_complex,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::keep_alive<0, 1>())
        .def("__setitem__", &CudaTensor::setitem_index,
            py::call_guard<py::gil_scoped_release>()
        )
        .def("__setitem__", &CudaTensor::setitem_simple,
            py::call_guard<py::gil_scoped_release>()
        )
        .def("__setitem__", &CudaTensor::setitem_complex,
            py::call_guard<py::gil_scoped_release>()
        )
        .def("__setitem__", &CudaTensor::fill_index,
            py::call_guard<py::gil_scoped_release>()
        )
        .def("__setitem__", &CudaTensor::fill_simple,
            py::call_guard<py::gil_scoped_release>()
        )
        .def("__setitem__", &CudaTensor::fill_complex,
            py::call_guard<py::gil_scoped_release>()
        )
        .def("fill", [](CudaTensor* t, double scalar) { fill(scalar, t); },
            py::call_guard<py::gil_scoped_release>()
        )
        .def("sum", &augpy::sum, "sum all values in tensor",
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("upcast")=false
        )
        .def("sum", &augpy::sum_axis, "sum all values in tensor",
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::arg("axis"),
            py::arg("keepdim")=false,
            py::arg("upcast")=false,
            py::arg("out")=(CudaTensor*)nullptr,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=0
        )
        .def("reshape", &CudaTensor::reshape,
            py::call_guard<py::gil_scoped_release>(),
            py::return_value_policy::take_ownership,
            py::keep_alive<0, 1>()
        )
        .def_property_readonly("itemsize", [](CudaTensor* t){
            return itemsize(t->dl_tensor.dtype);
        })
        .def_property_readonly("is_contiguous", &CudaTensor::is_contiguous)
        .def_property_readonly("dtype", [](CudaTensor* t){
            return t->dl_tensor.dtype;
        })
        .def_property_readonly("ndim", [](CudaTensor* t){
            return t->dl_tensor.ndim;
        })
        .def_property_readonly("shape", &CudaTensor::pyshape)
        .def_property_readonly("strides", &CudaTensor::pystrides)
        .def_property_readonly("byte_offset", [](CudaTensor* self) {
            return self->dl_tensor.byte_offset;
        })
        .def_property_readonly("size", [](CudaTensor* self) {
            return numel(self);
        })
        .def_property_readonly("ptr", [](CudaTensor* self) {
            return reinterpret_cast<size_t>(self->ptr());
        })
        .def("numpy", &tensor_to_array1,
            py::return_value_policy::take_ownership
        )
        .def("numpy", &tensor_to_array2,
            py::arg("array")=(py::buffer*)nullptr,
            py::return_value_policy::take_ownership
        );

    py::class_<RandomNumberGenerator> rng(m, "RandomNumberGenerator");
    rng
        .def(
            py::init<py::object*, py::object*>(),
            py::arg("device_id")=(py::object*)nullptr,
            py::arg("seed")=(py::object*)nullptr,
            py::return_value_policy::take_ownership
        )
        .def("uniform", &RandomNumberGenerator::uniform,
            py::arg("target"),
            py::arg("vmin"),
            py::arg("vmax"),
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=0
        )
        .def("gaussian", &RandomNumberGenerator::gaussian,
            py::arg("target"),
            py::arg("mean")=0.0,
            py::arg("std")=1.0,
            py::arg("blocks_per_sm")=BLOCKS_PER_SM,
            py::arg("threads")=0
        );

    py::class_<Decoder> decoder(m, "Decoder");
    decoder
        .def(
            py::init<size_t, size_t, bool>(),
            py::arg("device_padding")=16777216,
            py::arg("host_padding")=8388608,
            py::arg("gpu_huffman")=false
        )
        .def("decode", &Decoder::decode,
            py::call_guard<py::gil_scoped_release>(),
            py::arg("data"),
            py::arg("buffer")=(CudaTensor*)nullptr,
            py::return_value_policy::take_ownership,
            py::keep_alive<0, 3>()
        );

    m.def("import_dltensor", &import_dltensor,
        py::return_value_policy::take_ownership,
        py::keep_alive<0, 1>()
    );

    m.def("export_dltensor", &export_dltensor,
        py::return_value_policy::take_ownership,
        py::arg("tensor"),
        py::arg("name")="dltensor",
        py::arg("destruct")=true
    );

    m.def("tensor_to_array", &tensor_to_array1,
        py::arg("tensor"),
        py::return_value_policy::take_ownership
    );

    m.def("tensor_to_array", &tensor_to_array2,
        py::arg("tensor"),
        py::arg("array"),
        py::return_value_policy::take_ownership
    );

    m.def("array_to_tensor", &array_to_tensor1,
        py::arg("array"),
        py::arg("device_id")=0,
        py::return_value_policy::take_ownership
    );

    m.def("array_to_tensor", &array_to_tensor2,
        py::arg("array"),
        py::arg("tensor"),
        py::return_value_policy::take_ownership
    );

    m.def("make_affine_matrix", &make_affine_matrix,
        py::return_value_policy::take_ownership
    );

    py::enum_<WarpScaleMode>(m, "WarpScaleMode")
        .value("WARP_SCALE_SHORTEST", WarpScaleMode::WARP_SCALE_SHORTEST)
        .value("WARP_SCALE_LONGEST", WarpScaleMode::WARP_SCALE_LONGEST)
        .export_values();

    m.def("warp_affine", &warp_affine,
        py::arg("src"),
        py::arg("dst"),
        py::arg("matrix"),
        py::arg("background"),
        py::arg("supersampling"),
        py::return_value_policy::take_ownership,
        py::keep_alive<0, 2>()
    );

    m.def("add_gamma", &add_gamma, "add_gamma",
        py::call_guard<py::gil_scoped_release>(),
        py::arg("imtensor"),
        py::arg("gammagrays"),
        py::arg("gammacolors"),
        py::arg("contrasts"),
        py::arg("max_value"),
        py::arg("out")=(CudaTensor*)nullptr,
        py::return_value_policy::take_ownership
    );

    m.def("gaussian_blur", &gaussian_blur, "gaussian_blur",
        py::call_guard<py::gil_scoped_release>(),
        py::arg("input"),
        py::arg("sigmas"),
        py::arg("ksize"),
        py::arg("target")=(CudaTensor*)nullptr,
        py::return_value_policy::take_ownership
    );
    m.def("gaussian_blur_single", &gaussian_blur_single, "gaussian_blur_single",
        py::call_guard<py::gil_scoped_release>(),
        py::arg("input"),
        py::arg("sigma"),
        py::arg("target")=(CudaTensor*)nullptr,
        py::return_value_policy::take_ownership
    );
    m.def("box_blur_single", &box_blur_single, "box_blur_single",
        py::call_guard<py::gil_scoped_release>(),
        py::arg("input"),
        py::arg("ksize"),
        py::arg("target")=(CudaTensor*)nullptr,
        py::return_value_policy::take_ownership
    );

    py::register_exception<cuda_error>(m, "CudaError");
    py::register_exception<cnmem_error>(m, "MemoryError");
    py::register_exception<nvjpeg_error>(m, "NVJPEGError");
    py::register_exception<curand_error>(m, "CURandError");
    py::register_exception<cublas_error>(m, "CublasError");

    m.def("meminfo", &meminfo,
        py::arg("device_id")=0
    );
    m.def("enable_profiler", &enable_profiler);
    m.def("disable_profiler", &disable_profiler);
    m.def("nvtx_range_start", &nvtx_range_start);
    m.def("nvtx_range_end", &nvtx_range_end);
    m.def("init", &init);

    m.def("fma", &augpy::fma,
        "computes fma for float types and saturating fma for integer types",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("scalar"),
        py::arg("tensor1"),
        py::arg("tensor2"),
        py::arg("out")=(CudaTensor*)nullptr,
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=512
    );
    m.def("add", &add_scalar, "adds scalar to each element of tensor",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor"),
        py::arg("scalar"),
        py::arg("out")=(CudaTensor*)nullptr,
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=512
    );
    m.def("sub", &sub_scalar, "subtract scalar from each element of tensor",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor"),
        py::arg("scalar"),
        py::arg("out")=(CudaTensor*)nullptr,
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=512
    );
    m.def("rsub", &sub_scalar, "subtract each element of tensor from scalar",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor"),
        py::arg("scalar"),
        py::arg("out")=(CudaTensor*)nullptr,
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=512
    );
    m.def("mul", &mul_scalar, "multiplies tensor with scalar",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor"),
        py::arg("scalar"),
        py::arg("out")=(CudaTensor*)nullptr,
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=512
    );
    m.def("div", &div_scalar, "divides tensor by scalar",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor"),
        py::arg("scalar"),
        py::arg("out")=(CudaTensor*)nullptr,
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=512
    );
    m.def("rdiv", &div_scalar, "divides scalar by tensor",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor"),
        py::arg("scalar"),
        py::arg("out")=(CudaTensor*)nullptr,
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=512
    );
    m.def("add", &add_tensor, "adds tensors element wise",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor1"),
        py::arg("tensor2"),
        py::arg("out")=(CudaTensor*)nullptr,
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=512
    );
    m.def("sub", &sub_tensor, "adds tensors element wise",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor1"),
        py::arg("tensor2"),
        py::arg("out")=(CudaTensor*)nullptr,
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=512
    );
    m.def("mul", &mul_tensor, "multiplies tensors element wise",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor1"),
        py::arg("tensor2"),
        py::arg("out")=(CudaTensor*)nullptr,
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=512
    );
    m.def("div", &div_tensor, "divides tensors element wise",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor1"),
        py::arg("tensor2"),
        py::arg("out")=(CudaTensor*)nullptr,
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=512
    );
    m.def("cast", &cast_tensor,
        "cast tensor to target dtype or copy to target tensor",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor"),
        py::arg("result"),
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=0
    );
    m.def("cast", &cast_type,
        "cast tensor to target dtype or copy to target tensor",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor"),
        py::arg("dtype"),
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=0
    );
    m.def("gemm", &gemm, "cublas gemm wrapper",
        py::call_guard<py::gil_scoped_release>(),
        py::arg("A"),
        py::arg("B"),
        py::arg("C")=(CudaTensor*)nullptr,
        py::arg("alpha")=1.0,
        py::arg("beta")=0.0
    );

    m.def("copy", &copy, "copies the data tensor src to dst",
        py::call_guard<py::gil_scoped_release>(),
        py::arg("src"),
        py::arg("dst"),
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=0
    );

    m.def("fill", &augpy::fill, "fill dst tensor with scalar value",
        py::call_guard<py::gil_scoped_release>(),
        py::arg("scalar"),
        py::arg("dst"),
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("threads")=0
    );

    m.def("sum", &augpy::sum, "sum all values in tensor",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor"),
        py::arg("upcast")=false
    );

    m.def("sum", &augpy::sum_axis, "sum all values in tensor",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor"),
        py::arg("axis"),
        py::arg("keepdim")=false,
        py::arg("upcast")=false,
        py::arg("result")=(CudaTensor*)nullptr,
        py::arg("blocks_per_sm")=BLOCKS_PER_SM,
        py::arg("num_threads")=0
    );

    m.def("all", &augpy::all, "check truth value of all tensor elements",
        py::call_guard<py::gil_scoped_release>(),
        py::return_value_policy::take_ownership,
        py::arg("tensor")
    );
}
