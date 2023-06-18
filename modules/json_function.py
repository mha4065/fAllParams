from json import loads as json_loads


def extract_keys(obj):
    keys = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            keys.append(key)
            keys.extend(extract_keys(value))
    elif isinstance(obj, list):
        for item in obj:
            keys.extend(extract_keys(item))
    return keys


def json_params(response):
    try:
        data = json_loads(response.content)
        keys = extract_keys(data)
        keys = list(set(keys))
        return keys
    except ValueError:
        pass