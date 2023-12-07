

def depth_extractor(d: dict, key: str):
    if key in d:
        return d[key], d

    obj = None
    result_values = []

    for _key, _value in d.items():
        if isinstance(_value, dict):
            value, _obj = depth_extractor(_value, key)
            if value is not None and value:
                obj = _obj
                if isinstance(value, (list, tuple, set)):
                    result_values.extend(value)
                else:
                    result_values.append(value)
        if isinstance(_value, (list, set, tuple)):
            if not _value:
                continue
            for item in _value:
                if isinstance(item, dict):
                    value, _obj = depth_extractor(item, key)
                    if value is not None and value:
                        obj = _obj
                        if isinstance(value, (list, tuple, set)):
                            result_values.extend(value)
                        else:
                            result_values.append(value)
    return result_values, obj
