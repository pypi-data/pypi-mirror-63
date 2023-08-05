// core.h
#ifndef CUDA_CORE_H
#define CUDA_CORE_H


#include <cuda.h>
#include <cuda_runtime.h>


#ifndef MAX_MANAGED_DEVICES
#define MAX_MANAGED_DEVICES 2048
#endif


#ifndef BLOCKS_PER_SM
#define BLOCKS_PER_SM 8
#endif


#if __CUDA_ARCH__ == 300
#define CORES_PER_SM 192
#elif __CUDA_ARCH__ == 320
#define CORES_PER_SM 192
#elif __CUDA_ARCH__ == 350
#define CORES_PER_SM 192
#elif __CUDA_ARCH__ == 370
#define CORES_PER_SM 192
#elif __CUDA_ARCH__ == 500
#define CORES_PER_SM 128
#elif __CUDA_ARCH__ == 520
#define CORES_PER_SM 128
#elif __CUDA_ARCH__ == 530
#define CORES_PER_SM 128
#elif __CUDA_ARCH__ == 600
#define CORES_PER_SM 64
#elif __CUDA_ARCH__ == 610
#define CORES_PER_SM 128
#elif __CUDA_ARCH__ == 620
#define CORES_PER_SM 128
#elif __CUDA_ARCH__ == 700
#define CORES_PER_SM 64
#elif __CUDA_ARCH__ == 720
#define CORES_PER_SM 64
#elif __CUDA_ARCH__ == 750
#define CORES_PER_SM 64
#else
#define CORES_PER_SM 64
#endif


#define ceil_div(a, b) ((a) + (b) - 1) / (b)


#define ASSERT_TRUE(expr, message) if (!(expr)) { throw std::invalid_argument(message); }


namespace augpy {


void init_device(int device_id);


struct cudaDevicePropEx : cudaDeviceProp {
    int leastStreamPriority = 0;
    int greatestStreamPriority = 0;
};
cudaDevicePropEx get_device_properties(int device_id);


int get_num_cuda_cores(int device_id);


int cores_per_sm(int major, int minor);
int cores_per_sm(int device_id);


void release();


void managed_cudamalloc(void** ptr, size_t size, int device_id);


void managed_cudafree(void* ptr);


void managed_eventalloc(cudaEvent_t* event);


void managed_eventfree(cudaEvent_t event);


void mark_orphaned(void* ptr, cudaEvent_t event);


class CudaEvent {
public:
    CudaEvent();
    ~CudaEvent() noexcept(false);
    cudaEvent_t get_event();
    void record();
    bool query();
    void synchronize(int microseconds=100);
private:
    cudaEvent_t event;
};


class CudaStream {
public:
    CudaStream(int device_id, int priority);
    ~CudaStream() noexcept(false);
    cudaStream_t& get_stream();
    void activate();
    void deactivate();
    void synchronize(int microseconds=100);

private:
    int device_id;
    int priority;
    cudaStream_t stream;
    cudaStream_t previous_stream;
};


extern thread_local int current_device;
extern thread_local cudaStream_t current_stream;
extern const CudaStream default_stream;


// namespace augpy
}


// core.h
#endif
