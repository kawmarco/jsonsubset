from hypothesis.strategies import text, integers, floats
from hypothesis.strategies import none, lists, recursive
from hypothesis.strategies import booleans, dictionaries

#from https://hypothesis.readthedocs.io/en/latest/data.html#recursive-data
JSON_LIST = (
    recursive(
        none() | floats(allow_nan=False) | integers() | booleans() | text(),
        lambda children: lists(children)
    )
)

JSON_FULL = (
    recursive(
        none() | floats(allow_nan=False) | integers() | booleans() | text(),
        lambda children: lists(children)| dictionaries(text(), children)
    )
)

JSON_FULL_LITE = (
    recursive(
        none() | floats(allow_nan=False) | integers() | booleans() | text(),
        lambda children: lists(children)| dictionaries(text(), children),
        max_leaves=15
    )
)