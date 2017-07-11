cdef class Value:
    """
    This class is meant to:
        -Hold character offsets of a JSON structure
        -Provide a method that transforms the raw JSON string
         from .start to .end to a Python object in .get()

    This superclass delegates actual parsing to ujson.loads(), but
    subclasses are encouraged to implement faster parsing methods
    for their own specialised types.
    """

    cdef char* start
    cdef char* end

    cdef bytes raw(self)

cdef class StringValue(Value):
    cdef int safe
    cpdef str get(self)

cdef class NumberValue(Value):
    pass

cdef class NullValue(Value):
    pass

cdef class ObjectValue(Value):
    cdef dict obj

    cpdef dict get(self)
