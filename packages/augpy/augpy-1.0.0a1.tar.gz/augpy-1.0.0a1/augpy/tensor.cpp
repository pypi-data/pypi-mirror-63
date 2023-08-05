#include "tensor.h"
#include "exception.h"
#include <sstream>


using namespace std;


namespace augpy {


bool dldatatype_equals(DLDataType t1, DLDataType t2) {
    return t1.code == t2.code && t1.bits == t2.bits && t1.lanes == t2.lanes;
}


void assert_contiguous(CudaTensor* t) {
    if (!t) throw std::invalid_argument("tensor required");
    if (!t->is_contiguous()) throw std::invalid_argument("tensor must be contiguous");
}


std::string dldatatype_repr(DLDataType dtype) {
    std::stringstream s;
    s << "<DLDataType ";
    switch(dtype.code) {
    case kDLInt:
        s << "int";
        break;
    case kDLUInt:
        s << "uint";
        break;
    case kDLFloat:
        s << "float";
        break;
    }
    s << (int) dtype.bits;
    if (dtype.lanes > 1) {
        s << " x " << dtype.lanes << " lanes";
    }
    s << ">";
    return s.str();
}


inline void calc_shape_strides(
        DLTensor* tensor,
        int64_t* shape
) {
    int64_t stride = 1;
    for (int i=tensor->ndim-1; i>=0; i--) {
        tensor->strides[i] = stride;
        stride *= shape[i];
        tensor->shape[i] = shape[i];
    }
}


void dltensor_deleter(DLManagedTensor* tensor) {
    py::gil_scoped_acquire acquire;
    if (tensor->manager_ctx) {
        py::object* pytensor = (py::object*) tensor->manager_ctx;
        tensor->manager_ctx = NULL;
        delete pytensor;
    }
    py::gil_scoped_release release;
}


CudaTensor::CudaTensor(int64_t* shape, int ndim, DLDataType dtype, int device_id) {
    if (ndim > DLTENSOR_MAX_NDIM) {
        char buf[64];
        sprintf (buf, "tensors may not have more than %d dimensions", DLTENSOR_MAX_NDIM);
        throw std::invalid_argument(buf);
    }
    // setup the tensor details
    DLTensor& t = dl_tensor;
    t.ctx.device_type = kDLGPU;
    t.ctx.device_id = device_id;
    t.ndim = ndim;
    t.shape = this->shape.ptr();
    t.strides = this->strides.ptr();
    calc_shape_strides(&t, shape);
    t.dtype.code = dtype.code;
    t.dtype.bits = dtype.bits;
    t.dtype.lanes = dtype.lanes;
    t.byte_offset = 0;
    // setup management details
    manager_ctx = NULL;
    deleter = dltensor_deleter;
    owner = true;
    contiguous = true;
    // allocate memory
    size_t size = numel(&t) * itemsize(dtype);
    managed_cudamalloc(&t.data, size, device_id);
    managed_eventalloc(&event);
}


CudaTensor::CudaTensor(std::vector<int64_t> shape, DLDataType dtype, int device_id) :
        CudaTensor(shape.data(), shape.size(), dtype, device_id) {}


CudaTensor::CudaTensor(CudaTensor* parent, int ndim, int64_t* shape) {
    if (!parent) {
        throw std::invalid_argument("parent tensor was NULL");
    }
    memcpy((void*) &this->dl_tensor, (void*) &parent->dl_tensor, sizeof(DLTensor));
    DLTensor& t = dl_tensor;
    t.ndim = ndim;
    t.shape = this->shape.ptr();
    t.strides = this->strides.ptr();
    calc_shape_strides(&t, shape);
    manager_ctx = NULL;
    deleter = dltensor_deleter;
    owner = false;
    contiguous = check_contiguous(this);
    event = parent->get_event();
}


CudaTensor::CudaTensor(CudaTensor* parent, int ndim, int64_t* shape, int64_t* strides, int64_t byte_offset) {
    if (!parent) {
        throw std::invalid_argument("parent tensor was NULL");
    }
    memcpy((void*) &dl_tensor, (void*) &parent->dl_tensor, sizeof(DLTensor));
    dl_tensor.ndim = ndim;
    dl_tensor.shape = this->shape.ptr();
    memcpy(dl_tensor.shape, shape, sizeof(int64_t)*ndim);
    dl_tensor.strides = this->strides.ptr();
    memcpy(dl_tensor.strides, strides, sizeof(int64_t)*ndim);
    dl_tensor.byte_offset = byte_offset;
    manager_ctx = NULL;
    deleter = dltensor_deleter;
    owner = false;
    contiguous = check_contiguous(this);
    event = parent->get_event();
}


CudaTensor::CudaTensor(CudaTensor* parent) :
        CudaTensor(parent, parent->dl_tensor.ndim, parent->dl_tensor.shape) {}


CudaTensor::CudaTensor(DLManagedTensor* parent) {
    memcpy((void*) &dl_tensor, (void*) &parent->dl_tensor, sizeof(DLTensor));
    manager_ctx = NULL;
    deleter = NULL;
    owner = false;
    managed_eventalloc(&event);
}


CudaTensor::~CudaTensor() noexcept(false) {
    DLTensor& t = dl_tensor;
    if (manager_ctx && deleter) {
        deleter((DLManagedTensor*) this);
    }
    if (!owner || t.data == NULL) {
        return;
    }
    if (t.ctx.device_type == DLDeviceType::kDLGPU) {
        mark_orphaned(t.data, event);
        //managed_cudafree(t.data);
        //managed_eventfree(event);
    }
    else {
        switch (t.dtype.bits) {
            case 8:
                delete[] (int8_t*)t.data;
                break;
            case 16:
                delete[] (int16_t*)t.data;
                break;
            case 32:
                delete[] (int32_t*)t.data;
                break;
            case 64:
                delete[] (int64_t*)t.data;
                break;
        }
    }
}


void* CudaTensor::ptr() {
    return (void*) (((char*)dl_tensor.data) + dl_tensor.byte_offset);
}


void CudaTensor::record() {
    CUDA(cudaEventRecord(event, current_stream));
}


cudaEvent_t CudaTensor::get_event() {
    return event;
}


bool CudaTensor::is_contiguous() {
    return contiguous;
}


inline void decode_indices(
        size_t dim,
        py::object indices,
        int64_t shape,
        ssize_t& start,
        ssize_t& stop,
        ssize_t& step,
        ssize_t& slicelength
) {
    if (py::isinstance<py::slice>(indices)) {
        PyObject* slice = indices.ptr();
        if (PySlice_GetIndicesEx(slice, shape, &start, &stop, &step, &slicelength) < 0) {
            throw py::error_already_set();
        }
    }
    else if (py::isinstance<py::int_>(indices)) {
        start = py::cast<ssize_t>(indices);
        stop = start;
        step = 0;
        slicelength = 0;
    }
    else if (py::isinstance<py::none>(indices)) {
        start = 0;
        stop = shape;
        step = 1;
        slicelength = shape;
    }
    else {
        throw std::invalid_argument("indices must be int or slice");
    }
    if (start < -shape || start >= shape) {
        char buf[64];
        sprintf (buf, "index %zd is out of bounds for dimension %zu with length %zd", dim, start, shape);
        throw py::index_error(buf);
    }
    if (start < 0) start += shape;
    if (stop < 0) stop += shape;
}


inline ssize_t index(int ndim, ssize_t* indices, int64_t* strides) {
    ssize_t item = 0;
    for (int i=0; i<ndim; i++) {
        item += indices[i] * strides[i];
    }
    return item;
}


CudaTensor* CudaTensor::slice_complex(py::tuple slices) {
    DLTensor& t = dl_tensor;
    if (t.ndim == 0) {
        throw py::index_error("cannot index scalars");
    }
    int nslices = slices.size();
    if (nslices > t.ndim) {
        char buf[44];
        sprintf (buf, "too many indices for %d dim tensor", dl_tensor.ndim);
        throw py::index_error(buf);
    }

    int ndim = 0;
    ssize_t start[DLTENSOR_MAX_NDIM];
    ssize_t stop[DLTENSOR_MAX_NDIM];
    ssize_t step[DLTENSOR_MAX_NDIM];
    ssize_t slicelength[DLTENSOR_MAX_NDIM];
    for (size_t i=0; i<slices.size(); i++) {
        decode_indices(i, slices[i], t.shape[i], start[i], stop[i], step[i], slicelength[i]);
        if (slicelength[i]) ndim += 1;
    }
    int j = ndim;
    int64_t new_shape[DLTENSOR_MAX_NDIM];
    int64_t new_strides[DLTENSOR_MAX_NDIM];
    int64_t item_offset = 0;
    for (int i=slices.size()-1; i>=0; i--) {
        item_offset += t.strides[i] * start[i];
        if (slicelength[i] > 0) {
            j--;
            new_strides[j] = t.strides[i] * step[i];
            new_shape[j] = slicelength[i];
        }
    }
    for(int i=slices.size(); i<t.ndim; i++) {
        new_shape[ndim] = t.shape[i];
        new_strides[ndim] = t.strides[i];
        ndim += 1;
    }

    CudaTensor* child = new CudaTensor(this, ndim, new_shape, new_strides, item_offset * itemsize(t.dtype));
    return child;
}


CudaTensor* CudaTensor::slice_simple(py::slice slice) {
    size_t start, stop, step, slicelength;
    DLTensor& t = dl_tensor;
    if (t.ndim == 0) {
        throw py::index_error("cannot index scalars");
    }
    if (!slice.compute(t.shape[0], &start, &stop, &step, &slicelength)) {
        throw py::error_already_set();
    }
//    CudaTensor* child = new CudaTensor(this);
//    child->dl_tensor.byte_offset += start * t.strides[0] * itemsize(t.dtype);
//    child->dl_tensor.shape[0] = slicelength;
//    child->dl_tensor.strides[0] *= step;

    int64_t new_shape[DLTENSOR_MAX_NDIM];
    int64_t new_strides[DLTENSOR_MAX_NDIM];

    memcpy(new_shape, t.shape, t.ndim*sizeof(int64_t));
    memcpy(new_strides, t.strides, t.ndim*sizeof(int64_t));
    new_shape[0] = slicelength;
    new_strides[0] *=step;



    CudaTensor* child = new CudaTensor(this, t.ndim, new_shape, new_strides, t.byte_offset + start * t.strides[0] * itemsize(t.dtype));
    return child;
}


CudaTensor* CudaTensor::index(ssize_t i) {
    DLTensor& t = dl_tensor;
    if (t.ndim == 0) {
        throw py::index_error("cannot index scalars");
    }
    i += t.shape[0];
    i %= t.shape[0];
    if (i<0) {
        char buf[32];
        sprintf (buf, "%zd", i);
        throw pybind11::index_error(buf);
    }
    CudaTensor* child = new CudaTensor(
        this, t.ndim-1, &t.shape[1], &t.strides[1],
        t.byte_offset + i * t.strides[0] * itemsize(t.dtype)
   );
    return child;
}


void CudaTensor::setitem_index(ssize_t index, CudaTensor* src) {
    CudaTensor* dst = this->index(index);
    copy(src, dst);
    delete dst;
}


void CudaTensor::setitem_simple(py::slice slice, CudaTensor* src) {
    CudaTensor* dst = this->slice_simple(slice);
    copy(src, dst);
    delete dst;
}


void CudaTensor::setitem_complex(py::tuple slices, CudaTensor* src) {
    CudaTensor* dst = this->slice_complex(slices);
    copy(src, dst);
    delete dst;
}


void CudaTensor::fill_index(ssize_t index, double scalar) {
    CudaTensor* dst = this->index(index);
    fill(scalar, dst);
    delete dst;
}


void CudaTensor::fill_simple(py::slice slice, double scalar) {
    CudaTensor* dst = this->slice_simple(slice);
    fill(scalar, dst);
    delete dst;
}


void CudaTensor::fill_complex(py::tuple slices, double scalar) {
    CudaTensor* dst = this->slice_complex(slices);
    fill(scalar, dst);
    delete dst;
}


CudaTensor* CudaTensor::reshape(std::vector<int64_t> shape) {
    if (shape.size() > DLTENSOR_MAX_NDIM) {
        char buf[64];
        sprintf (buf, "tensors may not have more than %d dimensions", DLTENSOR_MAX_NDIM);
        throw std::invalid_argument(buf);
    }
    if (numel(&dl_tensor) != numel(shape)) {
        throw std::invalid_argument("number of elements must not change");
    }
    return new CudaTensor(this, (int) shape.size(), shape.data());
}


std::string CudaTensor::repr() {
    std::stringstream s;
    DLTensor& t = dl_tensor;
    s << "<CudaTensor shape=(";
    for (int i=0; i<t.ndim-1; i++) {
        s << t.shape[i] << ", ";
    }
    if (t.ndim > 0) {
        s << t.shape[t.ndim-1];
    }
    s << "), ";
    s << "device=" << t.ctx.device_id << ", ";
    s << "dtype=";
    switch(t.dtype.code) {
    case kDLInt:
        s << "int";
        break;
    case kDLUInt:
        s << "uint";
        break;
    case kDLFloat:
        s << "float";
        break;
    }
    s << (int) t.dtype.bits;
    if (t.dtype.lanes > 1) {
        s << ", " << t.dtype.lanes << " lanes";
    }
    s << ">";
    return s.str();
}


py::tuple CudaTensor::pyshape() {
    DLTensor& t = dl_tensor;
    py::tuple s = py::tuple(t.ndim);
    for (int i=0; i<t.ndim; i++) {
        s[i] = t.shape[i];
    }
    return s;
}


py::tuple CudaTensor::pystrides() {
    DLTensor& t = dl_tensor;
    py::tuple s = py::tuple(t.ndim);
    for (int i=0; i<t.ndim; i++) {
        s[i] = t.strides[i];
    }
    return s;
}


CudaTensor* empty_like(CudaTensor* tensor) {
    return new CudaTensor(
        tensor->dl_tensor.shape,
        tensor->dl_tensor.ndim,
        tensor->dl_tensor.dtype,
        tensor->dl_tensor.ctx.device_id
    );
}


bool check_contiguous(DLTensor* tensor) {
    if (!tensor->strides) return true;
    size_t last_address = 1;
    size_t n = 1;
    for (int i=0; i<tensor->ndim; i++) {
        if (tensor->strides[i] < 1) return false;
        n *= tensor->shape[i];
        last_address += (tensor->shape[i] - 1) * tensor->strides[i];
    }
    return n == last_address;
}


bool check_contiguous(CudaTensor* tensor) {
    return check_contiguous(&tensor->dl_tensor);
}


bool check_contiguous(py::buffer_info &array) {
    if (!array.strides.size()) return true;
    size_t last_address = 0;
    size_t n = 1;
    for (int i=0; i<array.ndim; i++) {
        if (array.strides[i] < 1) return false;
        n *= array.shape[i];
        last_address += (array.shape[i] - 1) * array.strides[i];
    }
    return n == last_address / array.itemsize + 1;
}


bool array_equals(int dim0, int ndim, int64_t* array1, int64_t* array2) {
    for (int i=dim0; i<ndim; i++) {
        if (array1[i] != array2[i]) {
            return false;
        }
    }
    return true;
}


void check_tensor(CudaTensor* tensor, size_t min_size, bool contiguous) {
    if (!tensor) {
        throw std::invalid_argument("tensor was NULL");
    }
    if (contiguous && !tensor->is_contiguous()) {
        throw std::invalid_argument("need contiguous tensor");
    }
    if (min_size && min_size > numbytes(tensor)) {
        throw std::invalid_argument("insufficient tensor memory");
    }
}


void check_same_device(DLTensor t1, DLTensor t2) {
    if(t1.ctx.device_id != t2.ctx.device_id) {
        throw std::invalid_argument("tensors must be on the same device");
    }
}


void check_same_dtype_device(DLTensor t1, DLTensor t2) {
    check_same_device(t1, t2);
    if(t1.dtype.code != t2.dtype.code && t1.dtype.bits == t2.dtype.bits) {
        throw std::invalid_argument("tensors must have same dtype");
    }
}


void check_same_dtype_device_shape(DLTensor t1, DLTensor t2) {
    check_same_dtype_device(t1, t2);
    if(t1.ndim != t2.ndim || !array_equals(0, t1.ndim, t1.shape, t2.shape)) {
        throw std::invalid_argument("tensors must have same shape");
    }
}


void calc_threads(unsigned int &threads, int device_id) {
    if (threads == 0) {
        threads = cores_per_sm(device_id);
    }
}


void calc_blocks_values_1d(
        DLTensor t,
        unsigned int &num_blocks,
        size_t &num,
        unsigned int &values_per_thread,
        unsigned int threads,
        unsigned int blocks_per_sm
){
    num = numel(t);
    int64_t vpt = values_per_thread;
    if (values_per_thread == 0) {
        blocks_per_sm = max(1U, blocks_per_sm);
        cudaDeviceProp props = get_device_properties(t.ctx.device_id);
        vpt = ceil_div(num, props.multiProcessorCount * blocks_per_sm * threads);
    }
    // make sure values_per_thread is valid
    // must fit into unsigned int
    values_per_thread = min(
        (int64_t)std::numeric_limits<unsigned int>().max(),
        vpt
    );
    // if num is small and there are many SMs, values_per_thread < 1
    // recalculate given the actual values_per_thread
    num_blocks = ceil_div(ceil_div(num, values_per_thread), threads);
}


void calc_blocks_values_nd(
        DLTensor t,
        dim3 &grid,
        size_t &count,
        unsigned int &values_per_thread,
        unsigned int threads,
        unsigned int blocks_per_sm
){
    count = 1;
    for (int dim=1; dim<t.ndim; dim++) {
        count *= t.shape[dim];
    }
    size_t num = numel(t);
    int64_t vpt = values_per_thread;
    if (values_per_thread == 0) {
        blocks_per_sm = max(1U, blocks_per_sm);
        cudaDeviceProp props = get_device_properties(t.ctx.device_id);
        vpt = ceil_div(num, props.multiProcessorCount * blocks_per_sm * threads);
    }
    // make sure values_per_thread is valid
    values_per_thread = min(
        // must fit into unsigned int
        (int64_t)std::numeric_limits<unsigned int>().max(),
        // cannot be bigger than shape[0]
        min(vpt, t.shape[0])
    );
    // if num is small and there are many SMs, values_per_thread < 1
    // recalculate given the actual values_per_thread
    grid.x = ceil_div(t.shape[0], values_per_thread);
    grid.y = ceil_div(count, threads);
    grid.z = 1;
}


void calculate_contiguous_strides(DLTensor t, ndim_array &contiguous_strides) {
    int64_t total_stride = 1;
    for (int dim=t.ndim-1; dim>=0; dim--) {
        contiguous_strides[dim] = total_stride;
        total_stride *= t.shape[dim];
    }
}


bool calculate_broadcast_strides(
        DLTensor t_src,
        DLTensor t_dst,
        ndim_array &src_strides,
        const int t_src_index
){
    bool broadcast = false;
    if(t_src.ndim <= t_dst.ndim) {
        for(int dim=0; dim<t_src.ndim; ++dim) {
            if(t_src.shape[dim] != t_dst.shape[dim]) {
                if(t_src.shape[dim] == 1) {
                    broadcast = true;
                    src_strides[dim] = 0;
                }
                else {
                    char buf[256];
                    sprintf(buf, "argument %d (dim %d=%ld) must broadcastable to output (dim %d=%ld)",
                            t_src_index, dim, t_src.shape[dim], dim, t_dst.shape[dim]);
                    throw std::invalid_argument(buf);
                }
            }
            else {
                src_strides[dim] = t_src.strides[dim];
            }
        }
        for(int dim=t_src.ndim; dim<t_dst.ndim; ++dim) {
            broadcast = true;
            src_strides[dim] = 0;
        }
    }
    else {
        char buf[256];
        sprintf(buf, "argument %d (%d dims) must broadcastable to output (%d dims)",
                t_src_index, t_src.ndim, t_dst.ndim);
        throw std::invalid_argument(buf);
    }
    return broadcast;
}


bool calculate_broadcast_output_shape(
        DLTensor t1,
        DLTensor t2,
        int &ndim,
        int64_t* shape
){
    bool broadcast = false;
    ndim = min(t1.ndim, t2.ndim);
    int dim = 0;
    for( ; dim<ndim; ++dim) {
        if(t1.shape[dim] != t2.shape[dim]) {
            if(t1.shape[dim] == 1 || t2.shape[dim] == 1) {
                broadcast = true;
                shape[dim] = max(t1.shape[dim], t2.shape[dim]);
            }
            else {
                throw std::invalid_argument("inputs must broadcastable");
            }
        }
        else {
            shape[dim] = t1.shape[dim];
        }
    }
    if(t2.ndim > t1.ndim) {
        for( ; dim < t2.ndim; ++dim) {
            shape[dim] = t2.shape[dim];
        }
    }
    if(t1.ndim > t2.ndim) {
        for( ; dim < t1.ndim; ++dim) {
            shape[dim] = t1.shape[dim];
        }
    }
    return broadcast;
}


bool calculate_broadcast_output_shape(
        DLTensor t1,
        DLTensor t2,
        int &ndim,
        ndim_array &shape
){
    return calculate_broadcast_output_shape(t1, t2, ndim, &shape[0]);
}


CudaTensor* create_output_tensor(CudaTensor** tensors, int n_tensors, bool allow_null) {
    // for all given tensors, check if they are null
    // if not null, use max of tensor shapes for every dimension
    ndim_array shape;
    int ndim = 0;
    for (int t=0; t<n_tensors; ++t) {
        if (!tensors[t]) {
            if (allow_null) continue;
            char buf[256];
            sprintf(buf, "required argument %d is None", t+1);
            throw std::invalid_argument(buf);
        }
        DLTensor &dlt = tensors[t]->dl_tensor;
        ndim = max(ndim, dlt.ndim);
        for (int dim=0; dim<dlt.ndim; ++dim) {
            shape[dim] = max(shape[dim], dlt.shape[dim]);
        }
    }
    // create the output tensor with the determined shape
    return new CudaTensor(
        &shape[0], ndim,
        tensors[0]->dl_tensor.dtype,
        tensors[0]->dl_tensor.ctx.device_id
    );
}


bool can_coalesce_dimension(std::vector<DLTensor> tensors, int dim_dst, int dim_src) {
    for (DLTensor &t: tensors) {
        if (!t.strides) continue;
        else if (dim_src >= t.ndim) continue;
        else if (t.shape[dim_src] <= 1) continue;
        else if (t.strides[dim_dst] != t.shape[dim_src] * t.strides[dim_src]) {
            return false;
        }
    }
    return true;
}


void coalesce_dimension(DLTensor &tensor, int dim_dst, int dim_src) {
    // tensor does not have dimension dim_src, no need to coalesce
    if (dim_src >= tensor.ndim) {
        return;
    }
    // tensor has 1 less dimension after coalesce
    --tensor.ndim;
    // merge shape of dim_src into dim_dst
    tensor.shape[dim_dst] *= tensor.shape[dim_src];
    // tensor does not have strides, skip this step
    if (!tensor.strides) {
        return;
    }
    // dim_dst strides with dim_src items now
    tensor.strides[dim_dst] = tensor.strides[dim_src];
}


void coalesce_dimensions(std::vector<DLTensor> &tensors) {
    int max_ndim = 0;
    for (DLTensor &t: tensors) {
        max_ndim = max(max_ndim, t.ndim);
    }
    for (int dim_src=max_ndim-1; dim_src>0; --dim_src) {
        if (can_coalesce_dimension(tensors, dim_src-1, dim_src)) {
            for(DLTensor &t: tensors) {
                coalesce_dimension(t, dim_src-1, dim_src);
            }
        }
    }
}


#define DTYPE_BYTES(code, bits) switch(bits) { \
    case(8): return code "1"; \
    case(16): return code "2"; \
    case(32): return code "4"; \
    case(64): return code "8"; \
    case(128): return code "16"; \
}


const char* dtype_to_format(DLDataType dtype) {
    switch(dtype.code) {
        case kDLInt: DTYPE_BYTES("i", dtype.bits); break;
        case kDLUInt: DTYPE_BYTES("u", dtype.bits); break;
        case kDLFloat: DTYPE_BYTES("f", dtype.bits); break;
    }
    char buf[64];
    sprintf(buf, "unknown DLDataType code %d, %d bits", dtype.code, dtype.bits);
    throw std::invalid_argument(buf);
}


py::array* tensor_to_array2(CudaTensor* tensor, py::buffer* array) {
    DLTensor t = tensor->dl_tensor;
    if (t.dtype.lanes > 1) {
        throw std::invalid_argument("cannot convert tensors with more than 1 lane to numpy");
    }
    CudaTensor* tmp;
    if (tensor->is_contiguous()) {
        tmp = tensor;
    }
    else {
        tmp = empty_like(tensor);
        copy(tensor, tmp);
        t = tmp->dl_tensor;
    }

    size_t size = itemsize(t.dtype);
    std::vector<ssize_t> shape;
    std::vector<ssize_t> strides;
    size_t bytes_per_item = itemsize(tmp->dl_tensor.dtype);
    for (int i=0; i < t.ndim; i++) {
        size *= t.shape[i];
        shape.push_back(t.shape[i]);
        if (t.strides != NULL) {
            strides.push_back(t.strides[i] * bytes_per_item);
        }
    }

    void* host_data;
    py::object handle;
    if (array) {
        py::buffer_info array_info = array->request();
        if (numbytes(tmp) > numbytes(array_info)) {
            throw std::invalid_argument("target array is too small");
        }
        host_data = (void*) array_info.ptr;
        handle = py::object(*array);
    }
    else {
        host_data = (void*) new unsigned char[size];
        handle = py::capsule(host_data, [](void *f) {
            unsigned char* host_data = reinterpret_cast<unsigned char*>(f);
            delete[] host_data;
        });
    }

    CUDA(cudaMemcpyAsync(host_data, tmp->ptr(), size,
                     cudaMemcpyDeviceToHost, current_stream));

    tmp->record();
    if (tmp != tensor) {
        delete tmp;
    }

    py::array* result = new py::array(
        py::dtype(dtype_to_format(t.dtype)),
        shape, // shape
        strides, // C-style contiguous strides for byte
        host_data,
        handle
    );
    return result;
}


py::array* tensor_to_array1(CudaTensor* tensor) {
    return tensor_to_array2(tensor, NULL);
}


#define DTYPE_BITS(code, bytes) switch(bytes) { \
    case(1): return DLDataType{code, 8, 1}; \
    case(2): return DLDataType{code, 16, 1}; \
    case(4): return DLDataType{code, 32, 1}; \
    case(8): return DLDataType{code, 64, 1}; \
    case(16): return DLDataType{code, 128, 1}; \
}


const DLDataType bufferinfo_to_dtype(py::buffer_info& buf) {
    std::string format = buf.format;
    if (format.length() == 1) {
        std::string formats_int("cbhilqn");
        std::string formats_uint("B?HILQN");
        std::string formats_float("fdeg");
        if (formats_int.find(format) != std::string::npos) {
            DTYPE_BITS(kDLInt, buf.itemsize)
        }
        else if (formats_uint.find(format) != std::string::npos) {
            DTYPE_BITS(kDLUInt, buf.itemsize)
        }
        else if (formats_float.find(format) != std::string::npos) {
            DTYPE_BITS(kDLFloat, buf.itemsize)
        }
    }
    std::stringstream msg;
    msg << "numpy dtype \"";
    msg << format << "\" is not supported by dlpack";
    throw std::invalid_argument(msg.str().c_str());
}


CudaTensor* array_to_tensor(py::buffer* array, CudaTensor* tensor, int device_id) {
    py::buffer_info array_info = array->request();
    py::gil_scoped_release release;

    size_t size = numbytes(array_info);
    if (!tensor) {
        std::vector<int64_t> shapev;
        for (ssize_t i=0; i<array_info.ndim; i++) {
            shapev.push_back(array_info.shape[i]);
        }
        DLDataType dtype = bufferinfo_to_dtype(array_info);
        tensor = new CudaTensor(shapev, dtype, device_id);
    }
    else {
        check_tensor(tensor, size);
        int64_t shape[DLTENSOR_MAX_NDIM];
        int64_t strides[DLTENSOR_MAX_NDIM];
        for (ssize_t i=0; i<array_info.ndim; i++) {
            shape[i] = array_info.shape[i];
            strides[i] = array_info.strides[i] / array_info.itemsize;
        }
        tensor = new CudaTensor(tensor, array_info.ndim, shape, strides, 0);
    }

    CUDA(cudaMemcpyAsync(tensor->ptr(), array_info.ptr, size,
                         cudaMemcpyHostToDevice, current_stream));
    tensor->record();
    return tensor;
}


CudaTensor* array_to_tensor1(py::buffer* array, int device_id) {
    return array_to_tensor(array, NULL, device_id);
}


CudaTensor* array_to_tensor2(py::buffer* array, CudaTensor* tensor) {
    return array_to_tensor(array, tensor, 0);
}


CudaTensor* import_dltensor(py::capsule* tensor_capsule, const char* name) {
    DLManagedTensor* dltensor = static_cast<DLManagedTensor*>(
        PyCapsule_GetPointer(tensor_capsule->ptr(), name)
    );
    if(!dltensor) {
        throw std::invalid_argument("need DLTensor capsule");
    }
    if(!check_contiguous(&dltensor->dl_tensor)) {
        throw std::invalid_argument("DLTensor is not contiguous");
    }
    CudaTensor* tensor = new CudaTensor(dltensor);

    return tensor;
}


void capsule_destructor(PyObject* obj) {
    const char* given_name = (const char*) PyCapsule_GetContext(obj);
    if (given_name) {
        // deleter is run if name is still equal to given name of capsule
        DLManagedTensor* tensor = (DLManagedTensor*) PyCapsule_GetPointer(obj, given_name);
        if (tensor) {
            tensor->deleter(tensor);
        }
        else {
            PyErr_Clear();
        }
    }
}


std::vector<char*> capsule_names;


inline const char* get_interned_name(std::string* name) {
    char* str = NULL;
    for (auto it = capsule_names.begin() ; it != capsule_names.end(); ++it) {
        if (strcmp(name->c_str(), *it) == 0) {
            str = *it;
            break;
        }
    }
    if (!str) {
        char* new_str = new char[name->length()+1];
        memcpy(new_str, name->c_str(), name->length()+1);
        capsule_names.push_back(new_str);
        str = new_str;
    }
    return str;
}


py::capsule* export_dltensor(py::object* pytensor, std::string* name, bool destruct) {
    CudaTensor* tensor = pytensor->cast<CudaTensor*>();
    if (tensor->manager_ctx) {
        throw std::invalid_argument("tensor is already exported");
    }
    // TODO byte_offset is ignored by PyTorch, this is a workaround
    tensor->dl_tensor.data = tensor->ptr();
    tensor->dl_tensor.byte_offset = 0;
    // workaround end

    tensor->manager_ctx = (void*) new py::object((const py::object &) *pytensor);
    const char* str = get_interned_name(name);
    py::capsule* capsule = new py::capsule((void*) tensor, str);
    if (destruct) {
        PyCapsule_SetDestructor(capsule->ptr(), capsule_destructor);
        PyCapsule_SetContext(capsule->ptr(), (void*) str);
    }
    return capsule;
}


thread_local bool cublas_initialized[MAX_MANAGED_DEVICES];
thread_local cublasHandle_t cublas_handles[MAX_MANAGED_DEVICES];


cublasHandle_t init_cublas(int device_id) {
    if (!cublas_initialized[device_id]) {
        CUDA(cudaSetDevice(device_id));
        CUBLAS(cublasCreate(&cublas_handles[device_id]));
        cublas_initialized[device_id] = true;
    }
    return cublas_handles[device_id];
}


//computes C = A * (alpha*B) + beta*C
CudaTensor* gemm(
        CudaTensor* A,
        CudaTensor* B,
        CudaTensor* C,
        double alpha,
        double beta
){
    assert_contiguous(A);
    assert_contiguous(B);
    DLTensor &ta = A->dl_tensor;
	DLTensor &tb = B->dl_tensor;

    CudaTensor* retval = NULL;
    if (!C) {
        retval = C = new CudaTensor({ta.shape[0], tb.shape[1]}, ta.dtype, ta.ctx.device_id);
    }

    assert_contiguous(C);
	DLTensor &tc = C->dl_tensor;

    if(ta.ndim!=2 || tb.ndim != 2 || tc.ndim != 2){
        throw std::invalid_argument("tensors needs to have 2 dimensions");
    }
    if(ta.shape[1] != tb.shape[0]) {
        throw std::invalid_argument("A.shape[1] must match B.shape[0]");
    }
    if(ta.shape[0] != tc.shape[0] || tb.shape[1] != tc.shape[1]) {
        throw std::invalid_argument("shape of C must match A*C");
    }

    int m = tb.shape[1];
    int n = ta.shape[0];
    int k = tb.shape[0];
    int l = ta.shape[1];
    float casted_alpha = (float) alpha;
    float casted_beta = (float) beta;
    cublasHandle_t handle = init_cublas(current_device);
    CUBLAS(cublasSetStream(handle, current_stream));
    CUBLAS(cublasSgemm(
        handle,
        CUBLAS_OP_N, CUBLAS_OP_N,
        m, n, k,
        &casted_alpha,
        (float*)B->ptr(), m,
        (float*)A->ptr(), l,
        &casted_beta,
        (float*)C->ptr(), m
    ));
    A->record();
    B->record();
    C->record();

    return retval;
}


// namespace augpy
}
