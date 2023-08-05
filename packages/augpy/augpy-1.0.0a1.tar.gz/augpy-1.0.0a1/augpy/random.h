#ifndef AUGPY_RANDOM_H
#define AUGPY_RANDOM_H


#include <curand.h>
#include <curand_kernel.h>
#include "tensor.h"


namespace augpy {


using rng_t = curandStateXORWOW_t;


class RandomNumberGenerator {
public:
    RandomNumberGenerator(py::object* device_id, py::object* seed);
    RandomNumberGenerator(int* device_id, unsigned long long* seed);
    ~RandomNumberGenerator() noexcept(false);

    void uniform(
        CudaTensor* target,
        double vmin,
        double vmax,
        unsigned int blocks_per_sm=BLOCKS_PER_SM,
        unsigned int threads=0
    );
    void gaussian(
        CudaTensor* target,
        double mean,
        double std,
        unsigned int blocks_per_sm=BLOCKS_PER_SM,
        unsigned int threads=0
    );

private:
    void init_device_state(int* device_id, unsigned long long* seed);
    int device_id;
    unsigned long long seed;

    curandGenerator_t gen;
    rng_t* device_states;
    size_t num_states;
};


// namespace augpy
}


// AUGPY_RANDOM_H
#endif
