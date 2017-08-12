# jsonsubset

[![CircleCI](https://circleci.com/gh/kawmarco/jsonsubset.svg?style=svg)](https://circleci.com/gh/kawmarco/jsonsubset)

jsonsubset is a [cython](http://cython.org/)-based JSON parser that is optimised to parse and extract only selected parts of a JSON string.

Its main idea is to attempt to extract a small number of fields out of a large JSON object [faster than a traditional JSON parser](#why-is-it-faster-than-parsing-the-whole-json) (i.e. one that always parses the whole JSON) would.

If you have a large amount of raw JSON objects and you need to extract only certain parts of it, jsonsubset may be able to do it more efficiently than traditional JSON parsers (like `ujson`).

# Installation
Using pip:
```
pip3 install jsonsubset
```

# Usage example
Say you have a large amount of raw (i.e. stringified) JSON objects like the one below:
```
raw_json_object = b"""
{
    "id": "this_is_an_id",
    "status": "shipped",
    "active": true,
    "partnumber": 1234567,
    "many": {
        "more": [
            "attributes"
        ]
    }
}
"""
```
To compile a parser that will only extract the `id` and `partnumber` fields, use `jsonsubset.compile` to compile an [expression](#writing-jsonsubset-expressions):
```
import jsonsubset

jsub_parser = jsonsubset.compile({
    "id": True,
    "partnumber": True, 
})
```
Then, use the `.parse()` method to parse and extract only selected fields:
```
parsed = jsub_parser.parse(unparsed_json_object)
# parsed = {'id': 'this_is_an_id', 'partnumber': 1234567}
```

# Writing jsonsubset expressions
The simplest jsonsubset expression is simply `True`, which parses the entire JSON:
```
expression = True

jsub_parser = jsonsubset.compile(expression)

parsed = jsub_parser.parse(b'{"a": "valid", "json": { "object": "string" }}')
# parsed = {'a': 'valid', 'json': {'object': 'string'}}
```

To parse only specific fields from a JSON object, simply define a dictionary with the desired keys and set the corresponding values as `True`:
```
expression = {
    "a": True
}

jsub_parser = jsonsubset.compile(expression)

parsed = jsub_parser.parse(b'{"a": "valid", "json": { "object": "string" }}')
# parsed = {'a': 'valid'}
```

Nesting expressions is allowed as well:
```
expression = {
    "a": {
        "b": {
            "c": True
        }
    }
}

jsub_parser = jsonsubset.compile(expression)

parsed = jsub_parser.parse(b'{"a": {"b": {"c": 1234, "something": "else"}, "look_a_boolean": true}}')
# parsed = {'a': {'b': {'c': 1234}}}
```

One way to express jsonsubset expressions (i.e. the ones accepted by `jsonsubset.compile()`) would be by the recursive definition below:
```
EXPR = True | DICT_EXPR
DICT_EXPR = { KEY_STRING : EXPR }
KEY_STRING = <string containing a valid JSON object key>
```

# Benchmarks
TODO

# FAQ
## Why is it faster than parsing the whole JSON?
jsonsubset will attempt to parse only the fields selected in a [expression](#writing-jsonsubset-expressions). Once all fields defined in the expression are found, jsonsubset will return early and ignore the rest of the JSON string (thus saving processing time by not parsing what's not interesting to the user).

A best case scenario for jsonsubset would be if all fields that are defined in the expression are at the beginning of the JSON string, e.g. given the expression `{'a': True}`:
```
{"a": "something_interesting", "b": "dont_care", "c": 123456}
                             ^jsonsubset will stop here
```
jsonsubset will stop parsing at the indicated point and return `{'a': 'something_interesting'}`.

## Why is it slower than parsing the whole JSON?
If you find that jsonsubset is slower than, say, `ujson` (which is pretty fast, and used internally by jsonsubset), it may be that your JSON is already pretty small, or your particular use case is hitting a rather slow path in jsonsubset.

For example, a worst-case scenario would be trying to extract a key that doesn't exist in the raw JSON. In this case, jsonsubset will parse the whole object (trying to find the key set in the expression) instead of returning early.

Currently, there are also some inefficiencies for parsing certain JSON types (i.e. it's always a good idea to benchmark first. If you find yourself parsing small JSON objects or is extracting most fields from the JSON, `ujson` might be a better bet).

In any case, speed improvements are planned for later versions of jsonsubset :-]

## Is it well tested on invalid/corrupt JSON strings?
Glad you asked! :smile: 

While there are some relevant test cases for handling invalid input (i.e. correctly raising `ValueError` on invalid input), we recommend that you use jsonsubset on strings that are known to be valid JSON, as invalid input cases are not currently the focus of this project (and, hence, not so thoroughly tested).

If you find that jsonsubset is not raising `ValueError` on an input that should, please feel free to [open an issue](https://github.com/kawmarco/jsonsubset/issues).

# Licence
jsonsubset is free software available under the [MIT licence](https://github.com/kawmarco/jsonsubset/blob/master/LICENSE).
