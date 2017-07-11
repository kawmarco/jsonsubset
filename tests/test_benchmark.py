import pytest
import hashlib

import ujson
import subset

SAMPLE_SIZE = 500

def test_bench_small_ujson(benchmark, small_json):
    bench = benchmark(lambda: parse_ujson(small_json))

def test_bench_small_json_subset(benchmark, small_json):
    expr = {"id": True, "status": True}
    bench = benchmark(lambda: parse_json_subset(small_json, expr))

def test_bench_medium_ujson(benchmark, medium_json):
    bench = benchmark(lambda: parse_ujson(medium_json))

def test_bench_medium_json_subset(benchmark, medium_json):
    expr = {"id": True, "status": True}
    bench = benchmark(lambda: parse_json_subset(medium_json, expr))

## utils ##
def parse_ujson(test_samples):
    for sample in test_samples:
        ujson.loads(sample)

def parse_json_subset(test_samples, expr):
    sub = subset.JsonSubset(expr)
    for sample in test_samples:
        sub.parse(sample)

def md5(x):
    return hashlib.md5(str(x).encode('utf-8')).hexdigest()

@pytest.fixture
def small_json():
    return [
        ujson.dumps({"id": md5(i), "status": md5(i+SAMPLE_SIZE), "i": i}).encode("utf-8")
        for i in range(SAMPLE_SIZE)
    ]

@pytest.fixture
def medium_json():
    return [
        ujson.dumps({
            "nested": {
                "list": [
                    i*2 for j in range(10)
                ],
                "a_number": i/3,
                "a_bool": True
            },
            "id": md5(i),
            "status": md5(i+SAMPLE_SIZE),
            "other_nested": {
                "a_bool": True,
                "a_null": None,
            },
            "i": i,
        }).encode("utf-8")
        for i in range(SAMPLE_SIZE)
    ]
