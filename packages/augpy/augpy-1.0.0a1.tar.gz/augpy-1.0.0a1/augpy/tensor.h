#ifndef AUGPY_TENSOR_H
#define AUGPY_TENSOR_H


#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cuda.h>
#include <cuda_runtime.h>
#include "dlpack.h"
#include "core.h"
#include "exception.h"


namespace py = pybind11;


#ifndef DLTENSOR_MAX_NDIM
#define DLTENSOR_MAX_NDIM 6
#endif

#ifndef BATCH_ARG_SIZE
#define BATCH_ARG_SIZE 16
#endif


namespace augpy {


template<typename T, int N>
struct array {
    T x[N];

    array() {
        memset((T*) &x, 0, sizeof(T)*N);
    }

    array(T* values, int n) {
        memcpy((T*) &x, values, sizeof(T)*n);
        if (n < N) {
            memset((T*) &x[n], 0, sizeof(T)*(N-n));
        }
    }

    __device__ __host__ __forceinline__
    T& operator[](size_t idx) {
        return x[idx];
    }

    __device__ __host__ __forceinline__
    const T& operator[](size_t idx) const {
        return x[idx];
    }
    __device__ __host__ __forceinline__
    T* ptr() {
        return (T*) &x;
    }
};


template<class T, class... Tail>
array<T, 1+sizeof...(Tail)> make_array(T head, Tail... tail) {
    constexpr int N = 1+sizeof...(Tail);
    T a[]{head, tail...};
    return array<T, N>(&a[0], N);
}


typedef array<int64_t, DLTENSOR_MAX_NDIM> ndim_array;
template<typename scalar_t>
using arg_array = array<scalar_t, BATCH_ARG_SIZE>;
typedef arg_array<float> float_array;
typedef arg_array<double> double_array;
typedef arg_array<int> int_array;
typedef arg_array<int64_t> int64_array;


const DLDataType dldtype_int8{kDLInt, 8, 1};
const DLDataType dldtype_uint8{kDLUInt, 8, 1};
const DLDataType dldtype_int16{kDLInt, 16, 1};
const DLDataType dldtype_uint16{kDLUInt, 16, 1};
const DLDataType dldtype_int32{kDLInt, 32, 1};
const DLDataType dldtype_uint32{kDLUInt, 32, 1};
const DLDataType dldtype_int64{kDLInt, 64, 1};
const DLDataType dldtype_uint64{kDLUInt, 64, 1};
const DLDataType dldtype_float16{kDLFloat, 16, 1};
const DLDataType dldtype_float32{kDLFloat, 32, 1};
const DLDataType dldtype_float64{kDLFloat, 64, 1};


std::string dldatatype_repr(DLDataType dtype);


template<typename scalar_t>
inline DLDataType get_dldatatype() {
    if (std::is_same<scalar_t, uint8_t>::value) return dldtype_uint8;
    else if (std::is_same<scalar_t, uint16_t>::value) return dldtype_uint16;
    else if (std::is_same<scalar_t, uint32_t>::value) return dldtype_uint32;
    else if (std::is_same<scalar_t, uint64_t>::value) return dldtype_uint64;
    else if (std::is_same<scalar_t, int8_t>::value) return dldtype_int8;
    else if (std::is_same<scalar_t, int16_t>::value) return dldtype_int16;
    else if (std::is_same<scalar_t, int32_t>::value) return dldtype_int32;
    else if (std::is_same<scalar_t, int64_t>::value) return dldtype_int64;
    else if (std::is_same<scalar_t, float>::value) return dldtype_float32;
    else if (std::is_same<scalar_t, double>::value) return dldtype_float64;
    else throw std::invalid_argument("dtype is not supported");
}


bool dldatatype_equals(DLDataType t1, DLDataType t2);


struct CudaTensor : DLManagedTensor {
public:
    CudaTensor(std::vector<int64_t> shape, DLDataType dtype, int device_id);
    CudaTensor(int64_t* shape, int ndim, DLDataType dtype, int device_id);
    CudaTensor(CudaTensor* parent, int ndim, int64_t* shape, int64_t* strides, int64_t byte_offset);
    CudaTensor(CudaTensor* parent, int ndim, int64_t* shape);
    CudaTensor(CudaTensor* parent);
    CudaTensor(DLManagedTensor* parent);
    ~CudaTensor() noexcept(false);

    void* ptr();
    void record();
    cudaEvent_t get_event();
    bool is_contiguous();
    CudaTensor* index(ssize_t i);
    CudaTensor* slice_simple(py::slice slice);
    CudaTensor* slice_complex(py::tuple slices);
    void setitem_index(ssize_t index, CudaTensor* src);
    void setitem_simple(py::slice slice, CudaTensor* src);
    void setitem_complex(py::tuple slices, CudaTensor* src);
    void fill_index(ssize_t index, double scalar);
    void fill_simple(py::slice slice, double scalar);
    void fill_complex(py::tuple slices, double scalar);
    CudaTensor* reshape(std::vector<int64_t> shape);
    std::string repr();
    py::tuple pyshape();
    py::tuple pystrides();

private:
    bool owner;
    bool contiguous;
    ndim_array shape;
    ndim_array strides;
    cudaEvent_t event;
};


void assert_contiguous(CudaTensor* t);


CudaTensor* fma(
    double scalar,
    CudaTensor* tensor1,
    CudaTensor* tensor2,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=0
);


CudaTensor* copy(
        CudaTensor* src,
        CudaTensor* dst,
        unsigned int blocks_per_sm=BLOCKS_PER_SM,
        unsigned int num_threads=0
);


void fill(
        double scalar,
        CudaTensor* dst,
        unsigned int blocks_per_sm=BLOCKS_PER_SM,
        unsigned int num_threads=0
);


CudaTensor* empty_like(CudaTensor* tensor);


template <typename scalar_t>
inline size_t numel(scalar_t* shape, size_t ndim) {
    size_t n = 1;
    for (size_t i=0; i<ndim; i++) {
        n *= shape[i];
    }
    return n;
}


template <typename scalar_t>
inline size_t numel(std::vector<scalar_t> &shape) {
    return numel(shape.data(), shape.size());
}


inline size_t numel(DLTensor* tensor) {
    return numel(tensor->shape, tensor->ndim);
}


inline size_t numel(DLTensor &tensor) {
    return numel(tensor.shape, tensor.ndim);
}


inline size_t numel(CudaTensor* tensor) {
    return numel(tensor->dl_tensor);
}


inline size_t numel(py::buffer_info &array) {
    return numel(array.shape);
}


inline size_t itemsize(DLDataType &dtype) {
    return (dtype.bits * dtype.lanes + 7) / 8;
}


inline size_t numbytes(DLTensor* tensor) {
    return numel(tensor) * itemsize(tensor->dtype);
}


inline size_t numbytes(CudaTensor* tensor) {
    return numbytes(&tensor->dl_tensor);
}


inline size_t numbytes(py::buffer_info &array) {
    return numel(array.shape) * array.itemsize;
}


bool check_contiguous(DLTensor* tensor);
bool check_contiguous(CudaTensor* tensor);
bool check_contiguous(py::buffer_info &array);


bool array_equals(int dim0, int ndim, int64_t* array1, int64_t* array2);


void check_tensor(CudaTensor* tensor, size_t min_size=0, bool contiguous=true);


void check_same_device(DLTensor t1, DLTensor t2);
void check_same_dtype_device(DLTensor t1, DLTensor t2);
void check_same_dtype_device_shape(DLTensor t1, DLTensor t2);


void calc_threads(unsigned int &threads, int device_id);


void calc_blocks_values_1d(
        DLTensor t,
        unsigned int &num_blocks,
        size_t &num,
        unsigned int &values_per_thread,
        unsigned int threads,
        unsigned int blocks_per_sm=BLOCKS_PER_SM
);


void calc_blocks_values_nd(
        DLTensor t,
        dim3 &grid,
        size_t &count,
        unsigned int &values_per_thread,
        unsigned int threads,
        unsigned int blocks_per_sm=BLOCKS_PER_SM
);


void calculate_contiguous_strides(DLTensor t, ndim_array &contiguous_strides);


bool calculate_broadcast_strides(
        DLTensor t_src,
        DLTensor t_dst,
        ndim_array &src_strides,
        const int t_src_index
);


bool calculate_broadcast_output_shape(
        DLTensor t1,
        DLTensor t2,
        int &ndim,
        int64_t* shape
);


bool calculate_broadcast_output_shape(
        DLTensor t1,
        DLTensor t2,
        int &ndim,
        ndim_array &shape
);


CudaTensor* create_output_tensor(CudaTensor** tensors, int n_tensors, bool allow_null);


void coalesce_dimensions(std::vector<DLTensor> &tensors);


py::array* tensor_to_array1(CudaTensor* tensor);


py::array* tensor_to_array2(CudaTensor* tensor, py::buffer* array);


CudaTensor* array_to_tensor1(py::buffer* array, int device_id=0);


CudaTensor* array_to_tensor2(py::buffer* array, CudaTensor* tensor);


CudaTensor* import_dltensor(py::capsule* tensor_capsule, const char* name);


py::capsule* export_dltensor(py::object* pytensor, std::string* name, bool destruct);


void cast_tensor(
        CudaTensor* tensor,
        CudaTensor* result,
        unsigned int blocks_per_sm=BLOCKS_PER_SM,
        unsigned int num_threads=0
);


CudaTensor* cast_type(
        CudaTensor* tensor,
        DLDataType dtype,
        unsigned int blocks_per_sm=BLOCKS_PER_SM,
        unsigned int num_threads=0
);


CudaTensor* gemm(
        CudaTensor* A,
        CudaTensor* B,
        CudaTensor* C,
        double alpha=1,
        double beta=0
);


CudaTensor* add_scalar(
    CudaTensor* tensor,
    double scalar,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* sub_scalar(
    CudaTensor* tensor,
    double scalar,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* rsub_scalar(
    CudaTensor* tensor,
    double scalar,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* mul_scalar(
    CudaTensor* tensor,
    double scalar,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* div_scalar(
    CudaTensor* tensor,
    double scalar,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* rdiv_scalar(
    CudaTensor* tensor,
    double scalar,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* lt_scalar(
    CudaTensor* tensor,
    double scalar,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* le_scalar(
    CudaTensor* tensor,
    double scalar,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* gt_scalar(
    CudaTensor* tensor,
    double scalar,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* ge_scalar(
    CudaTensor* tensor,
    double scalar,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* eq_scalar(
    CudaTensor* tensor,
    double scalar,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* add_tensor(
    CudaTensor* tensor1,
    CudaTensor* tensor2,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* sub_tensor(
    CudaTensor* tensor1,
    CudaTensor* tensor2,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* mul_tensor(
    CudaTensor* tensor1,
    CudaTensor* tensor2,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* div_tensor(
    CudaTensor* tensor1,
    CudaTensor* tensor2,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* lt_tensor(
    CudaTensor* tensor1,
    CudaTensor* tensor2,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* le_tensor(
    CudaTensor* tensor1,
    CudaTensor* tensor2,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);

CudaTensor* eq_tensor(
    CudaTensor* tensor1,
    CudaTensor* tensor2,
    CudaTensor* result,
    unsigned int blocks_per_sm=BLOCKS_PER_SM,
    unsigned int num_threads=512
);


// namespace augpy
}


// AUGPY_TENSOR_H
#endif
