cdef extern from "xxHash/xxhash.h":
    unsigned long long XXH64 (void* input, size_t length, unsigned long long seed)

cdef unsigned long long hash64(void* s, size_t s_len):
    return XXH64(s, s_len, 0)

def hash64_bytes(bytes bytes_string):
    cdef char* s = bytes_string
    cdef size_t s_len = len(bytes_string) * sizeof(char)
    return hash64(s, s_len)