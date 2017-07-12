from subset_expression cimport Expression

cdef object parse(bytes json_bytes, Expression* expr, int expr_len)
