# jsonsubset

jsonsubset is a [cython](http://cython.org/)-based JSON parser that is optimised to parse and extract only selected parts of a JSON string.

Its main use case is to extract a small number of fields out of a large JSON object.

If you have a large amount of raw JSON objects and is only interested in certain parts of it, jsonsubset may be able to do it more efficiently than traditional JSON parsers (like `ujson`) :-]

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
To compile a parser that will only extract the `id` and `partnumber` fields, use `jsonsubset.compile`:
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

# Benchmarks
TODO

# Licence
