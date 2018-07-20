from typing import Any, Dict, Optional, TypeVar

T = TypeVar('T')


def require(value: T) -> T:
    if value is None:
        return None
    else:
        return value

