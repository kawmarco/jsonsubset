from json_parser_values cimport *

cdef class Parser:
    cdef char* json_bytes
    cdef int json_bytes_len

    # this is needed to hold reference to the original byte string
    # so that the GC doesn't free it before we're done with it
    cdef object json_bytes_python

    cdef char* i

    cdef int num_parsed
    cdef int expr_len
    cdef object expr
    cdef char last

    cpdef object parse(self)
    cdef object _parse(self, object expr)

    cdef ObjectValue _parse_obj(self, expr)
    cdef StringValue _parse_str(self)
    cdef Value _parse_array(self)
    cdef NumberValue _parse_num(self)
    cdef NullValue _parse_null(self)
    cdef _parse_bool(self)
    cdef char consume(self)