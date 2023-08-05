// dispatch.h
#ifndef DISPATCH_H
#define DISPATCH_H


#include <stdio.h>
#include "dlpack.h"


namespace augpy {


#define __PRIVATE_CASE_TYPE(enum_type, SCALAR_T_NAME, scalar, sscalar, temp, ...) \
        case enum_type: {                                                         \
            using SCALAR_T_NAME = scalar;                                         \
            using sscalar_t = sscalar;                                            \
            using temp_t = temp;                                                  \
            __VA_ARGS__();                                                        \
            break;                                                                \
        }


#define __DISPATCH_FLOAT(BITS, SCALAR_T_NAME,NAME, ...)                           \
        __PRIVATE_CASE_TYPE(32, SCALAR_T_NAME, float, float, float, __VA_ARGS__);

#define __DISPATCH_DOUBLE(BITS, SCALAR_T_NAME, NAME, ...)                            \
        __PRIVATE_CASE_TYPE(64, SCALAR_T_NAME, double, double, double, __VA_ARGS__);


#define __DISPATCH_UINT_F(BITS, SCALAR_T_NAME, NAME, ...)                             \
        __PRIVATE_CASE_TYPE(8, SCALAR_T_NAME,uint8_t, int8_t, float, __VA_ARGS__);    \
        __PRIVATE_CASE_TYPE(16, SCALAR_T_NAME,uint16_t, int16_t, float, __VA_ARGS__);


#define __DISPATCH_UINT_D(BITS, SCALAR_T_NAME, NAME, ...)                               \
        __PRIVATE_CASE_TYPE(32, SCALAR_T_NAME, uint32_t, int32_t, double, __VA_ARGS__); \
        __PRIVATE_CASE_TYPE(64, SCALAR_T_NAME, uint64_t, int64_t, double, __VA_ARGS__);


#define __DISPATCH_INT_F(BITS, SCALAR_T_NAME, NAME, ...)                              \
        __PRIVATE_CASE_TYPE(8, SCALAR_T_NAME, int8_t, int8_t, float, __VA_ARGS__);    \
        __PRIVATE_CASE_TYPE(16, SCALAR_T_NAME, int16_t, int16_t, float, __VA_ARGS__); \


#define __DISPATCH_INT_D(BITS, SCALAR_T_NAME, NAME, ...)                               \
        __PRIVATE_CASE_TYPE(32, SCALAR_T_NAME, int32_t, int32_t, double, __VA_ARGS__); \
        __PRIVATE_CASE_TYPE(64, SCALAR_T_NAME, int64_t, int32_t, double, __VA_ARGS__);


#define THROW(NAME, CODE, BITS)                                                      \
    char msg[512];                                                                   \
    switch(CODE){                                                                    \
        case kDLInt:                                                                 \
            sprintf(msg, "failed to dispatch \"%s\" for dtype int%d", NAME, BITS);   \
            break;                                                                   \
        case kDLUInt:                                                                \
            sprintf(msg, "failed to dispatch \"%s\" for dtype uint%d", NAME, BITS);  \
            break;                                                                   \
        case kDLFloat:                                                               \
            sprintf(msg, "failed to dispatch \"%s\" for dtype float%d", NAME, BITS); \
            break;                                                                   \
    }                                                                                \
    throw std::invalid_argument(msg);


#define __DISPATCH(TYPE, SCALAR_T_NAME, NAME, ...){                        \
    uint8_t code = TYPE.code;                                              \
    unsigned char bits = TYPE.bits ;                                       \
    switch(code){                                                          \
        case kDLInt:                                                       \
            switch(bits){                                                  \
                __DISPATCH_INT_F(bits, SCALAR_T_NAME, NAME, __VA_ARGS__);  \
                __DISPATCH_INT_D(bits, SCALAR_T_NAME, NAME, __VA_ARGS__);  \
                default: THROW(NAME, code, bits)                           \
            }; break;                                                      \
        case kDLUInt:                                                      \
            switch(bits){                                                  \
                __DISPATCH_UINT_F(bits, SCALAR_T_NAME, NAME, __VA_ARGS__); \
                __DISPATCH_UINT_D(bits, SCALAR_T_NAME, NAME, __VA_ARGS__); \
                default: THROW(NAME, code, bits)                           \
            }; break;                                                      \
        case kDLFloat:                                                     \
            switch(bits){                                                  \
                __DISPATCH_FLOAT(bits, SCALAR_T_NAME, NAME, __VA_ARGS__);  \
                __DISPATCH_DOUBLE(bits, SCALAR_T_NAME, NAME, __VA_ARGS__); \
                default: THROW(NAME, code, bits)                           \
            }; break;                                                      \
        default:                                                           \
            THROW(NAME, code, bits)                                        \
    }                                                                      \
}


#define __DISPATCH_NOEXC(TYPE, SCALAR_T_NAME, NAME, ...){                  \
    uint8_t code = TYPE.code;                                              \
    unsigned char bits = TYPE.bits ;                                       \
    switch(code){                                                          \
        case kDLInt:                                                       \
            switch(bits){                                                  \
                __DISPATCH_INT_F(bits, SCALAR_T_NAME, NAME, __VA_ARGS__);  \
                __DISPATCH_INT_D(bits, SCALAR_T_NAME, NAME, __VA_ARGS__);  \
            }; break;                                                      \
        case kDLUInt:                                                      \
            switch(bits){                                                  \
                __DISPATCH_UINT_F(bits, SCALAR_T_NAME, NAME, __VA_ARGS__); \
                __DISPATCH_UINT_D(bits, SCALAR_T_NAME, NAME, __VA_ARGS__); \
            }; break;                                                      \
        case kDLFloat:                                                     \
            switch(bits){                                                  \
                __DISPATCH_FLOAT(bits, SCALAR_T_NAME, NAME, __VA_ARGS__);  \
                __DISPATCH_DOUBLE(bits, SCALAR_T_NAME, NAME, __VA_ARGS__); \
            }; break;                                                      \
    }                                                                      \
}


#define __DISPATCH_F(TYPE, SCALAR_T_NAME, NAME, ...){                      \
    uint8_t code = TYPE.code;                                              \
    unsigned char bits = TYPE.bits ;                                       \
    switch(code){                                                          \
        case kDLInt:                                                       \
            switch(bits){                                                  \
                __DISPATCH_INT_F(bits, SCALAR_T_NAME, NAME, __VA_ARGS__);  \
                default: THROW(NAME, code, bits)                           \
            }; break;                                                      \
        case kDLUInt:                                                      \
            switch(bits){                                                  \
                __DISPATCH_UINT_F(bits, SCALAR_T_NAME, NAME, __VA_ARGS__); \
                default: THROW(NAME, code, bits)                           \
            }; break;                                                      \
        case kDLFloat:                                                     \
            switch(bits){                                                  \
                __DISPATCH_FLOAT(bits, SCALAR_T_NAME, NAME, __VA_ARGS__);  \
                default: THROW(NAME, code, bits)                           \
            }; break;                                                      \
        default: THROW(NAME, code, bits)                                   \
    }                                                                      \


#define __DISPATCH_F_NOEXC(TYPE, SCALAR_T_NAME, NAME, ...){                \
    uint8_t code = TYPE.code;                                              \
    unsigned char bits = TYPE.bits ;                                       \
    switch(code){                                                          \
        case kDLInt:                                                       \
            switch(bits){                                                  \
                __DISPATCH_INT_F(bits, SCALAR_T_NAME, NAME, __VA_ARGS__);  \
            }; break;                                                      \
        case kDLUInt:                                                      \
            switch(bits){                                                  \
                __DISPATCH_UINT_F(bits, SCALAR_T_NAME, NAME, __VA_ARGS__); \
            }; break;                                                      \
        case kDLFloat:                                                     \
            switch(bits){                                                  \
                __DISPATCH_FLOAT(bits, SCALAR_T_NAME, NAME, __VA_ARGS__);  \
            }; break;                                                      \
    }                                                                      \
}


#define __DISPATCH_D(TYPE, SCALAR_T_NAME, NAME, ...){                      \
    uint8_t code = TYPE.code;                                              \
    unsigned char bits = TYPE.bits ;                                       \
    switch(code){                                                          \
        case kDLInt:                                                       \
            switch(bits){                                                  \
                __DISPATCH_INT_D(bits, SCALAR_T_NAME, NAME, __VA_ARGS__);  \
                default: THROW(NAME, code, bits)                           \
            }; break;                                                      \
        case kDLUInt:                                                      \
            switch(bits){                                                  \
                __DISPATCH_UINT_D(bits, SCALAR_T_NAME, NAME, __VA_ARGS__); \
                default: THROW(NAME, code, bits)                           \
            }; break;                                                      \
        case kDLFloat:                                                     \
            switch(bits){                                                  \
                __DISPATCH_DOUBLE(bits, SCALAR_T_NAME, NAME, __VA_ARGS__); \
                default: THROW(NAME, code, bits)                           \
            }; break;                                                      \
        default: THROW(NAME, code, bits)                                   \
    }                                                                      \
}


#define __DISPATCH_D_NOEXC(TYPE, SCALAR_T_NAME, NAME, ...){                \
    uint8_t code = TYPE.code;                                              \
    unsigned char bits = TYPE.bits ;                                       \
    switch(code){                                                          \
        case kDLInt:                                                       \
            switch(bits){                                                  \
                __DISPATCH_INT_D(bits, SCALAR_T_NAME, NAME, __VA_ARGS__);  \
            }; break;                                                      \
        case kDLUInt:                                                      \
            switch(bits){                                                  \
                __DISPATCH_UINT_D(bits, SCALAR_T_NAME, NAME, __VA_ARGS__); \
            }; break;                                                      \
        case kDLFloat:                                                     \
            switch(bits){                                                  \
                __DISPATCH_DOUBLE(bits, SCALAR_T_NAME, NAME, __VA_ARGS__); \
            }; break;                                                      \
    }                                                                      \
}


#define DISPATCH(TYPE, NAME, ...) __DISPATCH(TYPE, scalar_t, NAME, __VA_ARGS__)
#define DISPATCH_NOEXC(TYPE, NAME, ...) __DISPATCH_NOEXC(TYPE, scalar_t, NAME, __VA_ARGS__)

#define DISPATCH_F(TYPE, NAME, ...) __DISPATCH_F(TYPE, scalar_t, NAME, __VA_ARGS__)
#define DISPATCH_F_NOEXC(TYPE, NAME, ...) __DISPATCH_F_NOEXC(TYPE, scalar_t, NAME, __VA_ARGS__)

#define DISPATCH_D(TYPE, NAME, ...) __DISPATCH_D(TYPE, scalar_t, NAME, __VA_ARGS__)
#define DISPATCH_D_NOEXC(TYPE, NAME, ...) __DISPATCH_D_NOEXC(TYPE, scalar_t, NAME, __VA_ARGS__)


// namespace augpy
}


// dispatch.h
#endif
