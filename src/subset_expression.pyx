from libc.stdlib cimport malloc, free

import json
import xxhash

cdef Expression * compile(object expr):    
    if expr != True and type(expr) != dict:
        #XXX free on error
        raise ValueError("Invalid expression: " + repr(expr))

    cdef Expression* cexpr = new_expression()

    if expr is True:
        cexpr[0].is_leaf = 1
        assert cexpr.children.size() == 0
    
    else:
        cexpr[0].is_leaf = 0
        for key, value in expr.items():
            key_bytes = json.dumps(key).encode("utf-8")
            key_hash = xxhash.hash64_bytes(key_bytes)

            cexpr[0].children[0][key_hash] = compile(value)

        assert cexpr.children.size() == len(expr)

    return cexpr

cdef Expression* new_expression():
    cdef Expression* new_expr = <Expression*> malloc(sizeof(Expression))
    new_expr.flags = 0 
    new_expr.is_leaf = 0
    new_expr.children = new unordered_map[unsigned long long, Expression*]()
    return new_expr