from json import loads as json_loads

# Get all keys from JSON content-type
def get_keys(data):
    params = []
    for key in data.keys():
        params.append(key)
        if isinstance(data[key], dict):
            for sub_key in data[key].keys():
                params.append(sub_key)
                if isinstance(data[key][sub_key], dict):
                    for sub_sub_key in data[key][sub_key].keys():
                        params.append(sub_sub_key)
                        if isinstance(data[key][sub_key][sub_sub_key], dict):
                            for sub_sub_sub_key in data[key][sub_key][sub_sub_key].keys():
                                params.append(sub_sub_sub_key)
        elif isinstance(data[key], list):
            for item in data[key]:
                if isinstance(item, dict):
                    for sub_key in item.keys():
                        params.append(sub_key)
                        if isinstance(item[sub_key], dict):
                            for sub_sub_key in item[sub_key].keys():
                                params.append(sub_sub_key)
                                if isinstance(item[sub_key][sub_sub_key], dict):
                                    for sub_sub_sub_key in item[sub_key][sub_sub_key].keys():
                                        params.append(sub_sub_sub_key)
    params = list(set(params))
    return params


def json_params(response):
    data = json_loads(response.content)
    params = get_keys(data)
    return params