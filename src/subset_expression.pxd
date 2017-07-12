from libcpp.unordered_map cimport unordered_map

cdef struct Expression:
    int is_leaf
    unsigned int flags # user-definable flags
    unordered_map[unsigned long long, Expression*] *children

cdef Expression * compile(object expr)