from enum import Enum


def check_data_type(item):
    if isinstance(item, float):
        return Datatype.REAL
    elif isinstance(item, int):
        return Datatype.ITEGER
    elif isinstance(item, str):
        return Datatype.STRING
    else:
        return None


class Datatype(Enum):
    """
    Enum with integer types to be easily compared
    """
    ITEGER = 1
    STRING = 2
    REAL = 3
