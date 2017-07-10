import ujson

cdef class Parser:
    """
    This class concentrates all parser state and parsing methods for each type
    """
    cdef char* json_bytes
    cdef int json_bytes_len

    cdef char* i

    cdef int num_parsed
    cdef int expr_len
    cdef object expr

    def __cinit__(self, json_bytes_python, expr):
        self.json_bytes = self.i = json_bytes_python
        self.json_bytes_len = len(json_bytes_python)
        self.num_parsed = 0
        self.expr = expr

    def parse(self):
        return self._parse(self.expr)

    def _parse(self, expr):
        cdef char c = self.consume()

        if c == b'{':
            value = self._parse_obj(expr)

        if c == b'"':
            value = self._parse_str()

        elif c == b'[':
            value = self._parse_array()

        elif b'-' <= c <= b'9' or c in (b'I', b'N'): # 'I' -> "Infinity", 'N' -> NaN
            value = self._parse_num()

        else:
            # bug (or invalid json)
            assert False, (repr(self.json_bytes), int(self.i), repr(self.i))

        if expr == True:
            return value.get()

    cdef Value _parse_obj(self, expr):
        raise NotImplementedError()

    cdef StringValue _parse_str(self):
        cdef StringValue ret = StringValue()

        ret.start = self.i
        self.i += 1

        while self.i[0] != b'"':
            if self.i[0] == b'\\': #escaped char
                self.i += 2

            else:
                self.i += 1

        ret.end = self.i

        return ret

    cdef Value _parse_array(self):
        raise NotImplementedError()

    cdef _parse_num(self):
        cdef NumberValue ret = NumberValue()
        ret.start = self.i

        while (self.i[0] not in b' ,\x00}]'):
            self.i += 1

        ret.end = self.i - 1
        return ret

    cdef char consume(self):
        # just get next non-space character
        while self.i[0] == b' ':
            self.i += 1

        return self.i[0]

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

    def get(self):
        return ujson.loads(self.start[:self.end-self.start+1])

cdef class StringValue(Value):
    # TODO: Implement an optimised .get() method.
    # TIP: The naive implementation below doesn't work due to
    #      how JSON escapes unicode characters (with '\u' prefix):
    #
    # def get(self):
    #     return self.start[1:self.end-self.start].decode("utf-8")
    pass

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
