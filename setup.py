from setuptools import setup
from setuptools.extension import Extension

setup_requires = [
    'cython>=0.x',
    'pytest-runner',
]

install_requires = [
    'ujson',
]

tests_require = [
    'hypothesis',
    'pytest-benchmark',
    'pytest',
]

extensions = [
    Extension(
        "jsonsubset.deps.xxhash_cython.xxhash",
        [
            'jsonsubset/deps/xxhash_cython/xxhash.pyx',
            'jsonsubset/deps/xxhash_cython/xxHash/xxhash.c'
        ],
        include_dirs = ["jsonsubset/deps/xxhash_cython/xxHash"],
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
    name='jsonsubset',
    version='0.1.1',
    url='https://github.com/kawmarco/jsonsubset',
    description="Extract and parse specific fields from a JSON string ",
    author="Marco Kawajiri",
    keywords=[
        'jsonsubset',
        'json',
        'select',
    ],
    license="MIT license",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    packages=[
        "jsonsubset",
        "jsonsubset.deps.xxhash_cython",
    ],
    package_data={
        'jsonsubset': ['*.pxd'],
        "jsonsubset.deps.xxhash_cython": ['*.pxd'],
    },
    package_dir={
        'jsonsubset': 'jsonsubset',
        'jsonsubset.deps.xxhash_cython': 'jsonsubset/deps/xxhash_cython',

    },
    ext_modules=extensions,
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
)
