import pytest

import copy
from collections import defaultdict
import itertools

@pytest.fixture
def gen_expr():
    def _gen_expr(test_case):
        """
        Generates all possible jsonsubset expressions from a given test case
        """
        exprs = [True,] # True is always a valid expression

        if type(test_case) == dict:
            # generate all possible expressions for each key in test_case
            exprs_per_key = {
                key: _gen_expr(value) for key, value in test_case.items()
            }

            # combine all possible expressions from each key
            for n in range(1, len(test_case)+1):
                for key_set in itertools.combinations(test_case.keys(), n):
                    exprs.extend(
                        dict(key_expr) for key_expr in
                        itertools.product(*[
                            [(key, expr) for expr in exprs_per_key[key]] for key in key_set
                        ])
                    )

        return exprs
    return _gen_expr
