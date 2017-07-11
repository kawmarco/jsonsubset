import json
cimport json_parser

cdef class JsonSubset:
    cdef object compiled_expr
    cdef int expr_len

    def __init__(self, expr):
        self.compiled_expr = self._compile(expr)
        self.expr_len = self._expr_len(expr)

    def parse(self, bytes json_bytes):
        return json_parser.Parser(
            json_bytes,
            self.compiled_expr,
            self.expr_len
        ).parse()

    @classmethod
    def _compile(cls, expr):
        if expr == True:
            return expr

        if type(expr) == dict:
            return {
                json.dumps(key).encode("utf-8"): cls._compile(value)
                for key, value in expr.items()
            }

        raise ValueError("JsonSubset expression must be composed only of dicts and True, got " + repr(expr))

    @classmethod
    def _expr_len(cls, expr):
        if expr == True:
            return 1

        return sum(
            cls._expr_len(v) for v in expr.values()
        )
