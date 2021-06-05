from enum import Enum

from src.exceptions import BadDatatypeException


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
    ITEGER = "Integer"
    STRING = "String"
    REAL = "Real"


def convert(item, new_type: Datatype):
    try:
        if new_type == Datatype.REAL:
            return float(item)
        elif new_type == Datatype.STRING:
            return str(item)
        elif new_type == Datatype.ITEGER:
            return int(item)
    except Exception:
        raise BadDatatypeException(f"Cannot convert data \"{item}\" to {new_type}")
