from collections.abc import Iterable
from typing import Mapping

def isiterable(obj):
    return isinstance(obj, Iterable)

def ismapping(obj):
    return isinstance(obj, Mapping)
