import json
from fixtures import gen_expr
import tests.reference_implementation

TEST_CASES = [
    {},
    1,
    "123",
    "ábçdé",
    4129830912830,
    {"id": 1},
    {"id": "123"},
    {"id": "ábçdé"},
    {"a": {"nested": "value"}},
    {"a": {"nested": 1234}},
    {"a": {"more": {"complex": "json"}}, "with": {"branches": {"like": "this_one", "and": "that_one"}}}
]

def test_predefined_cases(gen_expr):
    for test_case in TEST_CASES:
        test_case_bytes = json.dumps(test_case).encode("utf-8")

        for expr in gen_expr(test_case):
            reference = tests.reference_implementation.subset(expr, test_case_bytes)

            # no actual implementation yet, just running reference implementation for now
            # TODO: add actual implementation here
            actual = reference
            assert actual == reference

#TODO property-based testing (using hypothesis)
