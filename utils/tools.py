from typing import get_type_hints


def value_pre_init(cls):
    type_hints = get_type_hints(cls)

    for key in type_hints.keys():
        setattr(cls, key, None)

    return cls

def set_dataclass_value(obj: object, dict_data: dict):
    type_hints = get_type_hints(obj)

    for key, value in dict_data.items():
        if isinstance(value, dict):
            cls = type_hints[key]
            new_instance = cls()
            set_dataclass_value(new_instance, value)
            value = new_instance

        setattr(obj, key, value)