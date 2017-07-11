import json
import ujson

cdef class Value:
    def get(self):
        return json.loads(self.start[:self.end-self.start+1].decode("utf-8"))

    cdef bytes raw(self):
        return self.start[:self.end-self.start+1]

cdef class StringValue(Value):
    cpdef str get(self):
        if self.safe:
            return self.start[1:self.end-self.start].decode("utf-8")
        return ujson.loads(self.start[:self.end-self.start+1])

cdef class NumberValue(Value):
    def get(self):
        # TODO: Benchmark and improve this code
        s = self.start[:self.end-self.start+1]

        if s == b'Infinity':
            return float('inf')

        elif s == b'-Infinity':
            return float('-inf')

        elif s == b'NaN':
            return float('nan')

        elif not b'.' in s and not b'e' in s:
            return int(s)

        else:
            return float(s)

cdef class NullValue(Value):
    def get(self):
        return None

cdef class ObjectValue(Value):
    cpdef dict get(self):
       return self.obj
