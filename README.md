# jsonsubset

jsonsubset is a cython-based JSON parser that is optimised to parse and extract only selected parts of a JSON string.

Its main use case is to extract a small number of fields out of a large JSON object. 

# Installation

`pip3 install jsonsubset`

# Usage example
Say you have a very large JSON object...
```
unparsed_json_object = b"""
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
...but you only need the values from, e.g. `id` and `partnumber`, you may compile a jsonsubset expression...
```
import jsonsubset

jsub_parser = jsonsubset.compile({
    "id": True,
    "partnumber": True, 
})
```
...and parse only selected fields using `.parse()`...
```
parsed_object = jsub_parser.parse(unparsed_json_object)
# parsed_object = {'id': 'this_is_an_id', 'partnumber': 1234567}
```

# Benchmarks
# TODO

# Licence
