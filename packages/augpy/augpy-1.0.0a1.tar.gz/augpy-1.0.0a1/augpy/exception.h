#ifndef AUGPY_EXCEPTION_H
#define AUGPY_EXCEPTION_H


#include <cstring>
#include <cuda_runtime.h>
#include <curand.h>
#include "cnmem.h"
#include <nvjpeg.h>
#include <cublas_v2.h>


namespace augpy {


#ifndef CUDA
#define CUDA(a) {cudaError_t _e = a; if(_e!=cudaSuccess){throw cuda_error(_e);}}
#endif
#ifndef CNMEM
#define CNMEM(a) {cnmemStatus_t _e = a; if(_e!=CNMEM_STATUS_SUCCESS){throw cnmem_error(_e);}}
#endif
#ifndef NVJPEG
#define NVJPEG(a) {nvjpegStatus_t _e = a; if(_e!=NVJPEG_STATUS_SUCCESS){throw nvjpeg_error(_e);}}
#endif
#ifndef CURAND
#define CURAND(a) {curandStatus_t _e = a; if(_e!=CURAND_STATUS_SUCCESS){throw curand_error(_e);}}
#endif
#ifndef CUBLAS
#define CUBLAS(a) {cublasStatus_t _e = a; if(_e!=CUBLAS_STATUS_SUCCESS){throw cublas_error(_e);}}
#endif




class cuda_error : std::exception{
public:
    cuda_error(cudaError_t error) : code(error) {}

    virtual const char* what() const noexcept{
        return cudaGetErrorString (code);
    }
private:
    cudaError_t code;
};


class cnmem_error : std::exception{
public:
    cnmem_error(cnmemStatus_t error) : code(error) {}

    virtual const char* what() const noexcept{
        return cnmemGetErrorString(code);
    }
private:
    cnmemStatus_t code;
};


class nvjpeg_error : std::exception{
public:
    nvjpeg_error(nvjpegStatus_t error) : code(error) {}

    virtual const char* what() const noexcept{
        switch(code){
        case NVJPEG_STATUS_NOT_INITIALIZED:
            return "nvjpeg returned \'NVJPEG_STATUS_NOT_INITIALIZED\'";
        case NVJPEG_STATUS_INVALID_PARAMETER:
            return "nvjpeg returned \'NVJPEG_STATUS_INVALID_PARAMETER\'";
        case NVJPEG_STATUS_BAD_JPEG:
            return "nvjpeg returned \'NVJPEG_STATUS_BAD_JPEG\'";
        case NVJPEG_STATUS_JPEG_NOT_SUPPORTED:
            return "nvjpeg returned \'NVJPEG_STATUS_JPEG_NOT_SUPPORTED\'";
        case NVJPEG_STATUS_ALLOCATOR_FAILURE:
            return "nvjpeg returned \'NVJPEG_STATUS_ALLOCATOR_FAILURE\'";
        case NVJPEG_STATUS_EXECUTION_FAILED:
            return "nvjpeg returned \'NVJPEG_STATUS_EXECUTION_FAILED\'";
        case NVJPEG_STATUS_ARCH_MISMATCH:
            return "nvjpeg returned \'NVJPEG_STATUS_ARCH_MISMATCH\'";
        case NVJPEG_STATUS_INTERNAL_ERROR:
            return "nvjpeg returned \'NVJPEG_STATUS_INTERNAL_ERROR\'";
        case NVJPEG_STATUS_IMPLEMENTATION_NOT_SUPPORTED:
            return "nvjpeg returned \'NVJPEG_STATUS_IMPLEMENTATION_NOT_SUPPORTED\'";
        case NVJPEG_STATUS_SUCCESS:
            return "nvjpeg returned no error \'NVJPEG_STATUS_SUCCESS\' THIS IS A BUG";
        default:
            return "UNKNOWN NVJPEG ERROR! THIS IS A BUG!";
        }
    }

private:
    nvjpegStatus_t code;
};


class curand_error : std::exception {
public:
    curand_error(curandStatus_t error) {
        this->code = error;
    }

    virtual const char* what() const noexcept{
        switch (code) {
        case CURAND_STATUS_SUCCESS:
            return "curand returned no error \'CURAND_STATUS_SUCCESS\' THIS IS A BUG";
        case CURAND_STATUS_VERSION_MISMATCH:
            return "curand returned \'CURAND_STATUS_VERSION_MISMATCH\'";
        case CURAND_STATUS_NOT_INITIALIZED:
            return "curand returned \'CURAND_STATUS_NOT_INITIALIZED\'";
        case CURAND_STATUS_ALLOCATION_FAILED:
            return "curand returned \'CURAND_STATUS_ALLOCATION_FAILED\'";
        case CURAND_STATUS_TYPE_ERROR:
            return "curand returned \'CURAND_STATUS_TYPE_ERROR\'";
        case CURAND_STATUS_OUT_OF_RANGE:
            return "curand returned \'CURAND_STATUS_OUT_OF_RANGE\'";
        case CURAND_STATUS_LENGTH_NOT_MULTIPLE:
            return "curand returned \'CURAND_STATUS_LENGTH_NOT_MULTIPLE\'";
        case CURAND_STATUS_DOUBLE_PRECISION_REQUIRED:
            return "curand returned \'CURAND_STATUS_DOUBLE_PRECISION_REQUIRED\'";
        case CURAND_STATUS_LAUNCH_FAILURE:
            return "curand returned \'CURAND_STATUS_LAUNCH_FAILURE\'";
        case CURAND_STATUS_PREEXISTING_FAILURE:
            return "curand returned \'CURAND_STATUS_PREEXISTING_FAILURE\'";
        case CURAND_STATUS_INITIALIZATION_FAILED:
            return "curand returned \'CURAND_STATUS_INITIALIZATION_FAILED\'";
        case CURAND_STATUS_ARCH_MISMATCH:
            return "curand returned \'CURAND_STATUS_ARCH_MISMATCH\'";
        case CURAND_STATUS_INTERNAL_ERROR:
            return "curand returned \'CURAND_STATUS_INTERNAL_ERROR\'";
        default:
            return "UNKNOWN CURAND ERROR! THIS IS A BUG!";
        }
    }

private:
    curandStatus_t code;
};

class cublas_error : std::exception{
public:
    cublas_error(cublasStatus_t error) : code(error) {}

    virtual const char* what() const noexcept{
        switch(code){
        case CUBLAS_STATUS_SUCCESS: return "CUBLAS_STATUS_SUCCESS";
        case CUBLAS_STATUS_NOT_INITIALIZED: return "CUBLAS_STATUS_NOT_INITIALIZED";
        case CUBLAS_STATUS_ALLOC_FAILED: return "CUBLAS_STATUS_ALLOC_FAILED";
        case CUBLAS_STATUS_INVALID_VALUE: return "CUBLAS_STATUS_INVALID_VALUE"; 
        case CUBLAS_STATUS_ARCH_MISMATCH: return "CUBLAS_STATUS_ARCH_MISMATCH"; 
        case CUBLAS_STATUS_MAPPING_ERROR: return "CUBLAS_STATUS_MAPPING_ERROR";
        case CUBLAS_STATUS_EXECUTION_FAILED: return "CUBLAS_STATUS_EXECUTION_FAILED"; 
        case CUBLAS_STATUS_INTERNAL_ERROR: return "CUBLAS_STATUS_INTERNAL_ERROR"; 
        default:return "unknown cublas error";
        }
    }
private:
    cublasStatus_t code;
};


// namespace augpy
}


// AUGPY_EXCEPTION_H
#endif
