import json
from hypothesis import given
from hypothesis.strategies import text

import json_parser

def test_init():
    prsr = json_parser.Parser(b'{}', True)

@given(text())
def test_str_simple(s):
    prsr = json_parser.Parser(json.dumps(s).encode("utf-8"), True)
    parsed = prsr.parse()
    assert parsed == s

@given(text(alphabet='a"\\', min_size=0, max_size=10))
def test_str_escaped_quotes_str(s):
    prsr = json_parser.Parser(json.dumps(s).encode("utf-8"), True)
    parsed = prsr.parse()
    assert parsed == s
