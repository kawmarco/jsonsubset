import pytest
import json
import random

from hypothesis import given
from hypothesis.strategies import text
from tests.hypothesis_strategies import JSON_FULL

from jsonsubset import json_parser

TEST_CASES = [
    '',
    '      ',
    ',',
    ':',
    '[',
    '[      ',
    '[1',
    '[1,',
    '[1,]',
    '[}',
    '[t'

    '{',
    '{      ',
    '{"',
    '{"1',
    '{"1"',
    '{"1":',
    '{"1":2',
    '{"1":2,',

    't',
    'f',

    'n',

    '"',
    '"\\',
    '":',
    '"        ',

    'I',
    '01',
    '000000.1',

    'a',
    'á',
    'asdiasodjq2oi3  123',
    '1asdasdasd'
]


def test_invalid_meta():
    # assert that json.loads() can't parse invalid test cases(otherwise it's a valid json 
    # and not a valid test case :-)
    for test_case_str in TEST_CASES:
        with pytest.raises(ValueError):
            json.loads(test_case_str)


def test_invalid_input():
    for test_case_str in TEST_CASES:
        parser = json_parser.Parser(test_case_str.encode("utf-8"), True, 1)
        with pytest.raises(ValueError):
            parser.parse()
        assert parser.consistent()

@given(JSON_FULL)
def test_invalid_input_random_corruption(test_case):
    json_chars = list(json.dumps(test_case))

    while True:
        try:
            test_case_str = "".join(json_chars)
            json.loads(test_case_str)
            json_chars[random.randint(0, len(json_chars)-1)] = chr(random.randint(0,128))

        except ValueError:
            break

    # XXX Ideally, it should follow json.loads() with value error if there's an error.
    # for now, though, we are happy if it doesn't overflow the string buffer or segfaults
    parser = json_parser.Parser(test_case_str.encode("utf-8"), True, 1)
    
    try:
        parser.parse()

    except ValueError:
        pass

    assert parser.consistent()

@given(text())
def test_invalid_input_non_json(s):
    try:
        json.loads(s)
        # valid json, skip test
        return
    
    except:
        pass

    # XXX Ideally, it should follow json.loads() with value error if there's an error.
    # for now, though, we are happy if it doesn't overflow the string buffer or segfaults
    parser = json_parser.Parser(s.encode("utf-8"), True, 1)
    try:
        parser.parse()

    except ValueError:
        pass

    assert parser.consistent()

@given(text(alphabet='{}[]\\tfIN01n:",-'))
def test_invalid_input_non_json_token_fuzzying(s):
    try:
        json.loads(s)
        # valid json, skip test
        return
    
    except:
        pass

    # XXX Ideally, it should follow json.loads() with value error if there's an error.
    # for now, though, we are happy if it doesn't overflow the string buffer or segfaults
    parser = json_parser.Parser(s.encode("utf-8"), True, 1)
    try:
        parser.parse()
    
    except ValueError:
        pass

    assert parser.consistent()
