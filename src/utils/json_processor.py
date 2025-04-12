import math


def replace_inf_values(obj: dict | list | float) -> dict | list | str | float:
    if isinstance(obj, dict):
        return {k: replace_inf_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_inf_values(v) for v in obj]
    elif isinstance(obj, float) and math.isinf(obj):
        return "Infinity" if obj > 0 else "-Infinity"
    return obj
