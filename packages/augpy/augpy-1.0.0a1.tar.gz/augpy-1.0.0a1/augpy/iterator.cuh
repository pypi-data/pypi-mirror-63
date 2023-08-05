#ifndef AUGPY_ITERATOR_CUH
#define AUGPY_ITERATOR_CUH


#include "tensor.h"
#include <iterator>
#include <iostream>


namespace augpy {


template<typename scalar_t>
struct tensor_iterator{
    unsigned char* it;
    const size_t count;
    const int ndim;
    const ndim_array strides;
    const ndim_array contiguous_strides;

    tensor_iterator(void* it, int ndim, ndim_array strides, ndim_arry contiguous_strides): 
        it(it), count(count), ndim(ndim), strides(strides), contiguous_strides(contiguous_strides) {}

    scalar_t operator[](size_t index) {
        // ensure ndim_arrays are put into registers or constant instead of local memory:
        //  - loop must be fixed length so it can be unrolled,
        //    thus indexing arrays with a constant value
        //  - exit the loop manually by testing against ndim
        //
        // See this section of the CUDA programming guide for details:
        // https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#device-memory-accesses
        #pragma unroll
        for(int i=1; i<DLTENSOR_MAX_NDIM; ++i) {
            if (i >= ndim) break;
            size_t p = index / contiguous_strides[i];
            it += p * strides[i];
            index %= contiguous_strides[i];
        }
        return *reinterpret_cast<scalar_t*>(it);
    }
};


template<typename scalar_t>
__device__ __host__ __forceinline__ scalar_t identity(const scalar_t& v) {
    return v;
}


template <typename scalar_t,
          typename transform_t,
          typename iterator_t=unsigned char*,
          typename offset_t=ptrdiff_t>
class TensorIterator{
public:
    typedef TensorIterator self_type;
    typedef offset_t difference_type;
    typedef scalar_t value_type;
    typedef scalar_t* pointer;
    typedef scalar_t reference;
    typedef std::random_access_iterator_tag iterator_category;

private:
    iterator_t it;
    offset_t contiguous_offset;
    const int ndim;
    const ndim_array strides;
    const ndim_array contiguous_strides;
    const transform_t transform;

public:
    __host__ __device__ __forceinline__ TensorIterator(iterator_t it, transform_t transform):
            it(it), transform(transform), {}

    __host__ __device__ __forceinline__ TensorIterator(TensorIterator* it, offset_t offset):
            transform(it->transform),
            it(it->it),
            contiguous_offset(it->contiguous_offset+offset),
            ndim(it->ndim),
            strides(it->strides),
            contiguous_strides(it->contiguous_strides){}

    /// Postfix increment
    __host__ __device__ __forceinline__ self_type operator++(int) {
        self_type retval = *this;
        contiguous_offset++;
        return retval;
    }

    /// Prefix increment
    __host__ __device__ __forceinline__ self_type operator++() {
        contiguous_offset++;
        return *this;
    }

    /// Indirection
    __host__ __device__ __forceinline__ reference operator*() const {
        return transform(this->[0]);
    }

    /// Addition
    template <typename distance_t>
    __host__ __device__ __forceinline__ self_type operator+(distance_t index) const {
        self_type retval(this, index);
        return retval;
    }

    /// Addition assignment
    template <typename distance_t>
    __host__ __device__ __forceinline__ self_type& operator+=(distance_t index) {
        contiguous_offset += index;
        return *this;
    }

    /// Subtraction
    template <typename distance_t>
    __host__ __device__ __forceinline__ self_type operator-(distance_t index) const {
        self_type retval(this, index);
        return retval;
    }

    /// Subtraction assignment
    template <typename distance_t>
    __host__ __device__ __forceinline__ self_type& operator-=(distance_t index) {
        contiguous_offset -= index;
        return *this;
    }

    /// Distance
    __host__ __device__ __forceinline__ difference_type operator-(self_type other) const {
        return contiguous_offset - other.contiguous_offset;
    }

    /// Array subscript
    template <typename distance_t>
    __host__ __device__ __forceinline__ reference operator[](distance_t index) const {
        iterator_t new_it = it;
        index += contiguous_offset;
        // ensure ndim_arrays are put into registers or constant instead of local memory:
        //  - loop must be fixed length so it can be unrolled,
        //    thus indexing arrays with a constant value
        //  - exit the loop manually by testing against ndim
        //
        // See this section of the CUDA programming guide for details:
        // https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#device-memory-accesses
        #pragma unroll
        for(int i=1; i<DLTENSOR_MAX_NDIM; ++i) {
            if (i >= ndim) break;
            size_t p = index / contiguous_strides[i];
            it += p * strides[i];
            index %= contiguous_strides[i];
        }
        return transform(*reinterpret_cast<scalar_t*>(new_it));
    }

    /// Structure dereference
    __host__ __device__ __forceinline__ pointer operator->() {
        return &transform(this->[0]);
    }

    /// Equal to
    __host__ __device__ __forceinline__ bool operator==(const self_type& other) {
        return it == other.it;
    }

    /// Not equal to
    __host__ __device__ __forceinline__ bool operator!=(const self_type& other) {
        return it != other.it;
    }

    /// ostream operator
    friend std::ostream& operator<<(std::ostream& os, const self_type& itr) {
        return os;
    }
};


// namespace augpy
}


// AUGPY_ITERATOR_CUH
#endif
