from typing import Generic, Optional, TypeVar

T = TypeVar('T')
D = TypeVar('D')

class Option(Generic[T]):
    '''Wraps an arbitrary, possibly `None` value in an object that is always
    defined. Not to be confused with the built-in `typing.Optional`.

    This can be used to dramatically simplify Qt Signal / Slot declarations.
    Qt "Slots" need to be decorated with the `class` of the data coming from the
    "Signal". A separate "connection" must be made between the Signal and Slot
    for each kind of data the Signal can emit (including optional values).
    If we wrap this data in `Option`, the Qt decorator is satisfied, and we
    can still specify the specific type in the Slot function parameters
    themselves.
    '''

    def __init__(self, value: Optional[T]):
        self._value = value

    def get(self) -> Optional[T]:
        return self._value

    def getOrDefault(self, default: D) -> 'T | D':
        return self._value or default

    def getOrRaise(self, err=Exception('None.get')) -> T:
        if self._value is None:
            raise err
        else:
            return self._value

    def isEmpty(self) -> bool:
        return self._value is None
