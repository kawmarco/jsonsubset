from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

sourcefiles = ['xxhash.pyx', 'xxHash/xxhash.c']

extensions = [
    Extension(
        "xxhash", 
        sourcefiles,
        extra_compile_args=[
            "-O3"
        ]
    )
]

setup(
    ext_modules = cythonize(extensions)
)