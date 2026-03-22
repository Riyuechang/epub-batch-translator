def set_dataclass_value(obj: object, dict_data: dict):
    for key, value in dict_data.items():
        if isinstance(value, dict):
            instance = getattr(obj, key)
            cls = instance if isinstance(instance, type) else type(instance)
            new_instance = cls()
            set_dataclass_value(new_instance, value)
            value = new_instance

        setattr(obj, key, value)