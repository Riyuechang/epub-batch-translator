from typing import Any, get_type_hints
from dataclasses import dataclass, fields


def dataclass_pre_init(cls):
    type_hints = get_type_hints(cls)

    for key in type_hints.keys():
        setattr(cls, key, None)

    return dataclass(cls)

def set_dataclass_value(obj: object, dict_data: dict):
    type_hints = get_type_hints(obj)

    for key, value in dict_data.items():
        cls = type_hints[key]

        if cls is Any:
            setattr(obj, key, value)
        elif isinstance(value, dict):
            new_instance = cls()
            set_dataclass_value(new_instance, value)
            setattr(obj, key, new_instance)
        else:
            setattr(obj, key, cls(value))

def get_dict(obj: object):
    return {f.name: getattr(obj, f.name) for f in fields(obj)}