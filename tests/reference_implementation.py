import json

def subset(expr, json_str):
    return _subset(expr, json.loads(json_str.decode("utf-8")))

def _subset(expr, parsed_json):
    if expr is True:
        return parsed_json

    elif type(parsed_json) != dict:
        return None

    return {
        key: (_subset(value, parsed_json[key]) if key in parsed_json else None)
        for key, value in expr.items()
    }
