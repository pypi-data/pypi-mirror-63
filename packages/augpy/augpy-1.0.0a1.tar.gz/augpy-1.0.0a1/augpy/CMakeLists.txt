cmake_minimum_required (VERSION 3.13)


project (cuda LANGUAGES CXX CUDA)


# enables fPIC
set(CMAKE_POSITION_INDEPENDENT_CODE ON)


# enable warnings for CXX only, nvcc does not understand these options
if (MSVC)
    add_compile_options($<$<COMPILE_LANGUAGE:CXX>:/W4>)
else()
    add_compile_options($<$<COMPILE_LANGUAGE:CXX>:-Wall>)
    add_compile_options($<$<COMPILE_LANGUAGE:CXX>:-Wextra>)
    add_compile_options($<$<COMPILE_LANGUAGE:CXX>:-pedantic>)
endif()


# define command line variables needed for python
set(PYINCLUDE "" CACHE STRING "Python include directories")
set(PYLIBDIRS "" CACHE STRING "Python library directories")
set(PYLIBS "" CACHE STRING "Python libraries to link")
set(PYLINKOPTIONS "" CACHE STRING "Python libraries to link")
set(PYSUFFIX "" CACHE STRING "Python shared library suffix")
set(CUDA_CCS "" CACHE STRING "Compute capabilities to build, e.g., 60")
separate_arguments(CUDA_CCS)


# define _augpy extension
add_library(_augpy SHARED
    cnmem/src/cnmem.cpp
    core.cpp
    tensor.cpp
    tensor_cast.cu
    tensor_cmp.cu
    tensor_copy.cu
    tensor_math.cu
    random.cu
    blur.cu
    gamma.cu
    warp_affine.cu
    reduce.cu
    nvjpegdecoder.cpp
    function.cpp
    module.cpp
)


set_target_properties(_augpy PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
set_target_properties(_augpy PROPERTIES PREFIX "")
set_target_properties(_augpy PROPERTIES SUFFIX "${PYSUFFIX}")
set_target_properties(_augpy PROPERTIES INTERPROCEDURAL_OPTIMIZATION TRUE)


target_compile_features(_augpy PUBLIC cxx_std_14)
target_link_directories(_augpy PUBLIC ${PYLIBDIRS})
target_link_libraries(_augpy ${PYLIBS} cudart curand nvjpeg cublas nvToolsExt )
target_link_options(_augpy PRIVATE
    $<$<COMPILE_LANGUAGE:CXX>:${PYLINKOPTIONS}>)
target_compile_options(_augpy PRIVATE
    $<$<COMPILE_LANGUAGE:CUDA>:-Xcompiler -fPIC --expt-relaxed-constexpr --use_fast_math>)


if(CMAKE_BUILD_TYPE MATCHES Debug)
target_compile_options(_augpy PRIVATE
    $<$<COMPILE_LANGUAGE:CUDA>:-lineinfo>)
target_compile_options(_augpy PRIVATE
    $<$<COMPILE_LANGUAGE:CUDA>:-Xptxas -v>)
endif()


foreach(V ${CUDA_CCS})
target_compile_options(_augpy PRIVATE
    $<$<COMPILE_LANGUAGE:CUDA>:-gencode=arch=compute_${V},code=sm_${V}>)
target_link_options(_augpy PRIVATE
    $<$<COMPILE_LANGUAGE:CUDA>:-arch=${V}>)
endforeach()


include_directories(
    ${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES}
    ${PYINCLUDE}
    dlpack
    cnmem/include
    cub
)
