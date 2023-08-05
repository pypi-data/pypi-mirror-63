#include <stdexcept>
#include <vector>
#include <mutex>
#include <algorithm>
#include <thread>
#include <chrono>
#include "core.h"
#include "exception.h"
#include "cnmem.h"


namespace augpy {


std::mutex device_mutex;
bool device_initialized[MAX_MANAGED_DEVICES];
cudaDevicePropEx device_properties[MAX_MANAGED_DEVICES];


void init_device(int device_id) {
    CUDA(cudaSetDevice(device_id));
    if (!device_initialized[device_id]) {
        cnmemStatus_t cnmem_e = CNMEM_STATUS_SUCCESS;
        cudaError_t cuda_e = cudaSuccess;
        device_mutex.lock();
        cuda_e = cudaSetDevice(device_id);
        // another thread may have initialized
        // between checking state and acquiring lock,
        // so check again if device is not yet initialized
        if (cuda_e == cudaSuccess && !device_initialized[device_id]) {
            cnmemDevice_t device{device_id, 1024*1024, 0, NULL, NULL};
            cnmemStatus_t cnmem_e = cnmemInit(1, &device, CNMEM_FLAGS_DEFAULT);
            device_initialized[device_id] = cnmem_e==CNMEM_STATUS_SUCCESS;
            cudaDevicePropEx* props = &device_properties[device_id];
            cuda_e = cudaGetDeviceProperties((cudaDeviceProp*)props, device_id);
            // if device supports stream priorities, get the range of valid priorities
            if (cuda_e == cudaSuccess) {
                cuda_e = cudaDeviceGetStreamPriorityRange(
                    &props->leastStreamPriority,
                    &props->greatestStreamPriority
                );
            }
        }
        device_mutex.unlock();
        if (cnmem_e != CNMEM_STATUS_SUCCESS){
            throw cnmem_error(cnmem_e);
        }
        if (cuda_e != cudaSuccess) {
            throw cuda_error(cuda_e);
        }
    }
}


cudaDevicePropEx get_device_properties(int device_id) {
    init_device(device_id);
    return device_properties[device_id];
}


int cores_per_sm(int major, int minor) {
    switch((major << 4) + minor) {
        case 0x30: return 192;
        case 0x32: return 192;
        case 0x35: return 192;
        case 0x37: return 192;
        case 0x50: return 128;
        case 0x52: return 128;
        case 0x53: return 128;
        case 0x60: return  64;
        case 0x61: return 128;
        case 0x62: return 128;
        case 0x70: return  64;
        case 0x72: return  64;
        case 0x75: return  64;
    }
    char msg[128];
    sprintf(msg, "unknown compute capability %d.%d", major, minor);
    throw std::invalid_argument(msg);
}


int cores_per_sm(int device_id) {
    cudaDeviceProp props = get_device_properties(device_id);
    return cores_per_sm(props.major, props.minor);
}


int get_num_cuda_cores(int device_id) {
    cudaDeviceProp props = get_device_properties(device_id);
    return cores_per_sm(props.major, props.minor) * props.multiProcessorCount;
}


void release() {
    device_mutex.lock();
    cnmemStatus_t e = cnmemFinalize();
    device_mutex.unlock();
    if(e!=CNMEM_STATUS_SUCCESS){
        throw cnmem_error(e);
    }
    for(int device_id=0; device_id<MAX_MANAGED_DEVICES; device_id++) {
        device_initialized[device_id] = 0;
    }
}


struct orphaned_memory {
    void* ptr;
    cudaEvent_t event;
};


// declare managed_eventfree_nolock
void managed_eventfree_nolock(cudaEvent_t event);


bool check_and_remove_orphaned(orphaned_memory mem) {
    cudaError_t e = cudaEventQuery(mem.event);
    if (e == cudaSuccess) {
        managed_cudafree(mem.ptr);
        managed_eventfree_nolock(mem.event);
        return true;
    }
    return false;
}


std::mutex manager_mutex;
std::vector<cudaEvent_t> event_pool[MAX_MANAGED_DEVICES];
std::vector<orphaned_memory> orphaned_memory_list[MAX_MANAGED_DEVICES];


void mark_orphaned(void* ptr, cudaEvent_t event) {
    manager_mutex.lock();
    orphaned_memory_list[current_device].push_back(orphaned_memory{ptr, event});
    manager_mutex.unlock();
}


void managed_cudamalloc(void** ptr, size_t size, int device_id) {
    init_device(device_id);
    manager_mutex.lock();
    std::vector<orphaned_memory> &orphans = orphaned_memory_list[current_device];
    orphans.erase(std::remove_if(
        orphans.begin(),
        orphans.end(),
        check_and_remove_orphaned
    ), orphans.end());
    manager_mutex.unlock();
    CNMEM(cnmemMalloc(ptr, size, current_stream));
}


void managed_cudafree(void* ptr) {
    CNMEM(cnmemFree(ptr, current_stream));
}


void managed_eventalloc(cudaEvent_t* event) {
    cudaError_t e = cudaSuccess;
    manager_mutex.lock();
    if (event_pool[current_device].size()) {
        *event = event_pool[current_device].back();
        event_pool[current_device].pop_back();
    }
    else {
        e = cudaEventCreateWithFlags(event, cudaEventBlockingSync | cudaEventDisableTiming);
    }
    manager_mutex.unlock();
    CUDA(e);
}


void managed_eventfree_nolock(cudaEvent_t event) {
    event_pool[current_device].push_back(event);
}


void managed_eventfree(cudaEvent_t event) {
    manager_mutex.lock();
    managed_eventfree_nolock(event);
    manager_mutex.unlock();
}


CudaEvent::CudaEvent() {
    managed_eventalloc(&event);
}


CudaEvent::~CudaEvent() noexcept(false) {
    managed_eventfree(event);
}


cudaEvent_t CudaEvent::get_event() {
    return event;
}


void CudaEvent::record() {
    CUDA(cudaEventRecord(event, current_stream));
}


bool CudaEvent::query() {
    cudaError_t e = cudaEventQuery(event);
    switch(e) {
    case cudaSuccess: return true;
    case cudaErrorNotReady: return false;
    default: throw cudaError(e);
    }
}


void CudaEvent::synchronize(int microseconds) {
    if (microseconds > 0) {
        std::chrono::microseconds delay(microseconds);
        cudaError_t e = cudaErrorNotReady;
        while (true) {
            e = cudaEventQuery(event);
            if (e != cudaErrorNotReady) {
                break;
            }
            std::this_thread::sleep_for(delay);
        }
        if (e == cudaSuccess) {
            return;
        }
        throw cudaError(e);
    }
    else {
        CUDA(cudaEventSynchronize(event));
    }
}


CudaStream::CudaStream(int device_id, int priority):
        device_id(device_id), priority(priority), stream(0), previous_stream(0) {
    // create proxy for default stream
    if (device_id == -1 && priority == -1) {
        return;
    }
    init_device(device_id);
    CUDA(cudaStreamCreateWithPriority(&stream, cudaStreamNonBlocking, priority));
    CNMEM(cnmemRegisterStream(stream));
}


CudaStream::~CudaStream() noexcept(false) {
    if (device_id != -1 && priority != -1) {
        CUDA(cudaStreamDestroy(stream));
    }
}


cudaStream_t& CudaStream::get_stream() {
    return stream;
}


void CudaStream::activate() {
    if (previous_stream) {
        throw std::invalid_argument("stream already active");
    }
    previous_stream = current_stream;
    current_stream = stream;
}


void CudaStream::deactivate() {
    if (!previous_stream) {
        throw std::invalid_argument("stream is not active");
    }
    current_stream = previous_stream;
    previous_stream = 0;
}


void CudaStream::synchronize(int microseconds) {
    if (microseconds > 0) {
        std::chrono::microseconds delay(microseconds);
        cudaError_t e = cudaErrorNotReady;
        while (true) {
            e = cudaStreamQuery(stream);
            if (e != cudaErrorNotReady) {
                break;
            }
            std::this_thread::sleep_for(delay);
        }
        if (e == cudaSuccess) {
            return;
        }
        throw cudaError(e);
    }
    else {
        CUDA(cudaStreamSynchronize(stream));
    }
}


thread_local cudaStream_t current_stream(0);
const CudaStream default_stream = CudaStream(-1, -1);
thread_local int current_device(0);


// namespace augpy
}
