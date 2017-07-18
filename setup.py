from setuptools import setup
from distutils.extension import Extension

setup_requires = [
    'cython>=0.x',
    'pytest-runner',
]

install_requires = [
    'ujson',
]

tests_require = [
    'pytest',
    'pytest-benchmark',
    'hypothesis',
]

extensions = [
    Extension(
        "jsonsubset.deps.xxhash_cython.xxhash",
        [
            'jsonsubset/deps/xxhash_cython/xxhash.pyx',
            'jsonsubset/deps/xxhash_cython/xxHash/xxhash.c'
        ],
        extra_compile_args=["-O3"]
    ),
    Extension(
        "jsonsubset.subset",
        ['jsonsubset/subset.pyx'],
        language='c++',
        extra_compile_args=["-O3"]
    ),
    Extension(
        "jsonsubset.json_parser",
        ['jsonsubset/json_parser.pyx'],
        language='c++',
        extra_compile_args=["-O3"]
    ),
]

setup(
    packages=["jsonsubset"],
    package_data={
        "jsonsubset.deps.xxhash_cython.xxhash": ["jsonsubset/deps/xxhash_cython/xxhash.pxd"],
    },
    package_dir={
        'jsonsubset': 'jsonsubset'
    },
    ext_modules=extensions,
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
)
