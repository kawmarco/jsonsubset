import json
import math

from hypothesis import given
from hypothesis.strategies import text, integers, floats
from hypothesis.strategies import none, lists, recursive
from hypothesis.strategies import booleans, dictionaries

import json_parser

#from https://hypothesis.readthedocs.io/en/latest/data.html#recursive-data
JSON_LIST = (
    recursive(none() | floats(allow_nan=False) | integers() | booleans() | text(),
    lambda children: lists(children))
)

JSON_FULL = (
    recursive(none() | floats(allow_nan=False) | integers() | booleans() | text(),
    lambda children: lists(children)| dictionaries(text(), children))
)

def test_init():
    parser = json_parser.Parser(b'{}', True)

@given(text())
def test_str_simple(s):
    parser = json_parser.Parser(json.dumps(s).encode("utf-8"), True)
    parsed = parser.parse()
    assert parsed == s

@given(text(alphabet='a"\\', min_size=0, max_size=10))
def test_str_escaped_quotes_str(s):
    parser = json_parser.Parser(json.dumps(s).encode("utf-8"), True)
    parsed = parser.parse()
    assert parsed == s

@given(integers())
def test_num_integers(i):
    parser = json_parser.Parser(json.dumps(i).encode("utf-8"), True)
    parsed = parser.parse()

    assert parsed == i
    assert type(parsed) == type(i)

@given(floats())
def test_num_floats(i):
    parser = json_parser.Parser(json.dumps(i).encode("utf-8"), True)
    parsed = parser.parse()

    assert (
        parsed == i or
        math.isnan(parsed) and math.isnan(i)
    )
    assert type(parsed) == type(i)

def test_null():
    parser = json_parser.Parser(json.dumps(None).encode("utf-8"), True)
    parsed = parser.parse()

    assert parsed == None

@given(booleans())
def test_bool(b):
    parser = json_parser.Parser(json.dumps(b).encode("utf-8"), True)
    parsed = parser.parse()

    assert parsed == b

@given(JSON_LIST)
def test_array(a):
    parser = json_parser.Parser(json.dumps(a).encode("utf-8"), True)
    parsed = parser.parse()

    assert parsed == a


@given(JSON_FULL)
def test_obj(obj):
    parser = json_parser.Parser(json.dumps(obj).encode("utf-8"), True)
    parsed = parser.parse()

    assert parsed == obj
