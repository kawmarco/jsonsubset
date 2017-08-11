# jsonsubset

jsonsubset is a [cython](http://cython.org/)-based JSON parser that is optimised to parse and extract only selected parts of a JSON string.

Its main use case is to extract a small number of fields out of a large JSON object.

If you have a large amount of raw JSON objects and you need to extract only certain parts of it, jsonsubset may be able to do it more efficiently than traditional JSON parsers (like `ujson`) :-]

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
To compile a parser that will only extract the `id` and `partnumber` fields, use `jsonsubset.compile` to compile an [expression](#Writing-jsonsubset-expressions):
```
import jsonsubset

jsub_parser = jsonsubset.compile({
    "id": True,
    "partnumber": True, 
})
```
Then, use the `.parse()` method to parse and extract only selected fields:
```
parsed_object = jsub_parser.parse(unparsed_json_object)
# parsed_object = {'id': 'this_is_an_id', 'partnumber': 1234567}
```

# Writing jsonsubset expressions
jsonsubset expressions (i.e. the ones accepted by `jsonsubset.compile()`) can be recursively defined by:
```
EXPR = True | DICT_EXPR
DICT_EXPR = { KEY_STRING : EXPR }
KEY_STRING = <string containing a valid JSON object key>
```

The simplest jsonsubset expression is simply `True`, which parses the entire JSON:
```
expression = True

jsub_parser = jsonsubset.compile(expression)

print(jsub_parser.parse(b'{"a": "valid", "json": { "object": "string" }}'))
# prints {'a': 'valid', 'json': {'object': 'string'}}
```

To parse only specific fields from a JSON object, simply define a dictionary with the desired keys and set the corresponding values as `True`:
```
expression = {
    "a": True
}

jsub_parser = jsonsubset.compile(expression)

print(jsub_parser.parse(b'{"a": "valid", "json": { "object": "string" }}'))
# prints {'a': 'valid'}
```

You can nest expressions as well:
```
expression = {
    "a": {
        "b": {
            "c": True
        }
    }
}

jsub_parser = jsonsubset.compile(expression)

print(jsub_parser.parse(b'{"a": {"b": {"c": 1234, "something": "else"}, "look_a_boolean": true}}'))
# prints jsub_parser = jsonsubset.compile({
    "a": {
        "b": {
            "c": True
        }
    }
})

print(jsub_parser.parse(b'{"a": {"b": {"c": 1234, "something": "else"}, "look_a_boolean": true}}'))
# prints {'a': {'b': {'c': 1234}}}
```

# Benchmarks
TODO

# Licence
