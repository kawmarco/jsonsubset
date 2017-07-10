import json
import math

from hypothesis import given
from hypothesis.strategies import text, integers, floats

import json_parser

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
