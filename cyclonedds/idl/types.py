"""
 * Copyright(c) 2021 ADLINK Technology Limited and others
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v. 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0, or the Eclipse Distribution License
 * v. 1.0 which is available at
 * http://www.eclipse.org/org/documents/edl-v10.php.
 *
 * SPDX-License-Identifier: EPL-2.0 OR BSD-3-Clause
"""

import typing
if not typing.TYPE_CHECKING:
    class NewType:
        def __init__(self, name, tp):
            self.__name__ = name
            self.__supertype__ = tp

        def __call__(self, x):
            return x

        def __repr__(self):
            return self.__name__
    typing.NewType = NewType

from typing import ClassVar, NewType, Sequence, Dict, Any, Optional, Type
from enum import Enum
from .type_helper import Annotated, get_origin, get_args, get_type_hints


char = NewType("char", int)
wchar = NewType("wchar", int)
int8 = NewType("int8", int)
int16 = NewType("int16", int)
int32 = NewType("int32", int)
int64 = NewType("int64", int)
uint8 = NewType("uint8", int)
uint16 = NewType("uint16", int)
uint32 = NewType("uint32", int)
uint64 = NewType("uint64", int)
float32 = NewType("float32", float)
float64 = NewType("float64", float)
NoneType = type(None)

primitive_types = {
    char: (1, 'b'),
    wchar: (2, 'h'),
    int8: (1, 'b'),
    int16: (2, 'h'),
    int32: (4, 'i'),
    int64: (8, 'q'),
    uint8: (1, 'B'),
    uint16: (2, 'H'),
    uint32: (4, 'I'),
    uint64: (8, 'Q'),
    float32: (4, 'f'),
    float64: (8, 'd'),
    int: (8, 'q'),
    bool: (1, '?'),
    float: (8, 'd')
}


def _type_repr(obj):
    """Avoid printing <class 'int'>"""
    if isinstance(obj, type):
        if obj.__module__ == 'builtins':
            return obj.__qualname__
        return f'{obj.__module__}.{obj.__qualname__}'
    if obj is ...:
        return '...'
    return repr(obj)


class GetItemSupportMeta(type):
    """__class_getitem__ is new in Python 3.7, this makes it work on 3.6"""
    def __getitem__(cls, tup):
        return cls.__class_getitem__(tup)


class array(metaclass=GetItemSupportMeta):
    @classmethod
    def __class_getitem__(cls, tup):
        if type(tup) != tuple:
            tup = (tup,)

        if len(tup) != 2 or type(tup[1]) != int:
            raise TypeError("An array takes two arguments: an element type and a constant length.")
        return Annotated[Sequence[tup[0]], cls(*tup)]

    def __init__(self, subtype: Type, length: int):
        self.subtype: Type = subtype
        self.length: int = length

    def __repr__(self) -> str:
        return f"array[{_type_repr(self.subtype)}, {self.length}]"

    def __eq__(self, o: object) -> bool:
        return isinstance(o, array) and o.subtype == self.subtype and o.length == self.length

    def __hash__(self) -> int:
        return (241813571056069 * self.length) ^ hash(self.subtype)

    __str__ = __repr__


class sequence(metaclass=GetItemSupportMeta):
    @classmethod
    def __class_getitem__(cls, tup):
        if type(tup) != tuple:
            tup = (tup,)

        if len(tup) not in [1, 2] or (len(tup) == 2 and type(tup[1]) != int):
            raise TypeError("A sequence takes a subtype and an optional maximum length.")
        if len(tup) > 1 and (tup[1] <= 0 or tup[1] > 65535):
            return TypeError("Sequence max length should be between 0 and 65536.")
        return Annotated[Sequence[tup[0]], cls(*tup)]

    def __init__(self, subtype: Type, max_length: Optional[int] = None) -> None:
        self.subtype: Type = subtype
        self.max_length: Optional[int] = max_length

    def __repr__(self) -> str:
        if self.max_length:
            return f"sequence[{_type_repr(self.subtype)}, {self.max_length}]"
        else:
            return f"sequence[{_type_repr(self.subtype)}]"

    def __eq__(self, o: object) -> bool:
        return isinstance(o, sequence) and o.subtype == self.subtype and o.max_length == self.max_length

    def __hash__(self) -> int:
        if self.max_length:
            return (406820761152607 * self.max_length) ^ hash(self.subtype)
        else:
            return 406820761152609 ^ hash(self.subtype)

    __str__ = __repr__


class bounded_str(metaclass=GetItemSupportMeta):
    @classmethod
    def __class_getitem__(cls, tup):
        if type(tup) != tuple:
            tup = (tup,)

        if len(tup) != 1 or type(tup[0]) != int:
            raise TypeError("A bounded str takes one argument, a maximum length.")
        if tup[0] <= 0:
            return TypeError("Bound string max length should be bigger than 0.")
        return Annotated[str, cls(*tup)]

    def __init__(self, max_length: int) -> None:
        self.max_length: int = max_length

    def __repr__(self) -> str:
        return f"bounded_str[{self.max_length}]"

    def __eq__(self, o: object) -> bool:
        return isinstance(o, bounded_str) and o.max_length == self.max_length

    def __hash__(self) -> int:
        return 277146416319491 * self.max_length

    __str__ = __repr__


class ValidUnionHolder:
    pass


class case(ValidUnionHolder, metaclass=GetItemSupportMeta):
    @classmethod
    def __class_getitem__(cls, tup):
        if type(tup) != tuple:
            tup = (tup,)

        if len(tup) != 2:
            raise TypeError("A case takes two arguments: the discriminator value(s) and the type.")
        return Annotated[Optional[tup[1]], cls(*tup)]

    def __init__(self, discriminator_value, subtype: Type) -> None:
        self.discriminator_value = discriminator_value
        self.subtype = subtype

    def __repr__(self) -> str:
        return f"case[{self.discriminator_value}, {_type_repr(self.subtype)}]"

    def __eq__(self, o: object) -> bool:
        return isinstance(o, case) and o.subtype == self.subtype and \
               o.discriminator_value == self.discriminator_value

    def __hash__(self) -> int:
        return (545464105755071 * self.discriminator_value) ^ hash(self.subtype)

    __str__ = __repr__


class default(ValidUnionHolder, metaclass=GetItemSupportMeta):
    @classmethod
    def __class_getitem__(cls, tup):
        if type(tup) != tuple:
            tup = (tup,)

        if len(tup) != 1:
            raise TypeError("A default takes one arguments: the type.")
        return Annotated[Optional[tup[0]], cls(*tup)]

    def __init__(self, subtype: Type) -> None:
        self.subtype: Type = type

    def __repr__(self) -> str:
        return f"default[{_type_repr(self.subtype)}]"

    def __eq__(self, o: object) -> bool:
        return isinstance(o, default) and o.subtype == self.subtype

    def __hash__(self) -> int:
        return 438058395842377 ^ hash(self.subtype)

    __str__ = __repr__


class IdlUnion:
    def __init__(self, **kwargs):
        self.discriminator = None
        self.value = None

        if 'discriminator' in kwargs:
            self.discriminator = kwargs['discriminator']
            self.value = kwargs.get('value')
        elif kwargs:
            for k, v in kwargs.items():
                self.__setattr__(k, v)
                break

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self._field_set:
            case = self._field_set[name]
            self.discriminator = case[0]
            self.value = value
            return
        if self._default and self._default[0] == name:
            self.discriminator = None
            self.value = value
            return
        return super().__setattr__(name, value)

    def __getattr__(self, name: str) -> Any:
        if name in self._field_set:
            _case = self._field_set[name]
            if self.discriminator != _case[0]:
                raise AttributeError("Tried to get inactive case on union")
            return self.value
        if self._default and self._default[0] == name:
            if self.discriminator is not None:
                raise AttributeError("Tried to get inactive case on union")
            return self.value
        return super().__getattribute__(name)

    def set(self, discriminator, value):
        self.discriminator = discriminator
        self.value = value

    def __repr__(self):
        return f"{self.__name__}[Union](discriminator={self.discriminator}, value={self.value})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.__name__ == other.__name__ and \
               self.discriminator == other.discriminator and \
               self.value == other.value


def _union_default_finder(type, cases):
    if isinstance(type, Enum):
        # We assume the enum is well formatted and starts at 0. We will use an integer to encode.
        return -1

    val, inc, end = {
        int8: (-1, -1, -128),
        int16: (-1, -1, -32768),
        int32: (-1, -1, -2147483648),
        int64: (-1, -1, -9223372036854775808),
        uint8: (0, 1, 255),
        uint16: (0, 1, 65535),
        uint32: (0, 1, 4294967295),
        uint64: (0, 1, 18446744073709551615),
    }.get(type, (None, None, None))

    if val is None:
        raise TypeError("Invalid discriminator type")

    while True:
        if val not in cases:
            return val
        if val == end:
            raise TypeError("No space in discriminated union for default value.")
        val += inc


map = Dict
optional = Optional  # TODO


def make_union(name, discriminator, fields, key=False):
    cases = {}
    field_set = {}
    default_ = None

    for field, _type in fields.items():
        if get_origin(_type) == ClassVar:
            continue

        if get_origin(_type) != Annotated:
            raise TypeError("Fields of a union need to be case or default.")

        tup = get_args(_type)
        if len(tup) != 2:
            raise TypeError("Fields of a union need to be case or default.")

        holder = tup[1]
        if type(holder) == tuple:
            # Edge case for python 3.6: bug in backport? TODO: investigate and report
            holder = holder[0]

        if not isinstance(holder, ValidUnionHolder):
            raise TypeError("Fields of a union need to be case or default.")

        if isinstance(holder, case):
            if type(holder.discriminator_value) == list:
                for d in holder.discriminator_value:
                    if d in cases:
                        raise TypeError(f"Discriminator values must uniquely define a case, "
                                        f"but the case {d} occurred multiple times.")
                    cases[d] = (field, holder.subtype)
                    if field not in field_set:
                        field_set[field] = (d, holder.subtype)
            else:
                d = holder.discriminator_value
                if d in cases:
                    raise TypeError(f"Discriminator values must uniquely define a case, "
                                    f"but the case {d} occurred multiple times.")
                cases[d] = (field, holder.subtype)
                if field not in field_set:
                    field_set[field] = (d, holder.subtype)
        else:  # isinstance(ValidUnionHolder) guarantees this is a default
            if default_ is not None:
                raise TypeError("A discriminated union can only have one default.")
            default_ = (field, holder.subtype)

    class MyUnionMeta(type):
        __class__ = name
        __name__ = name
        __qualname__ = name

        def __repr__(self):
            cdata = ", ".join(f"{field}: {type}" for field, type in fields.items())
            return f"{name}[{discriminator.__name__}]({cdata})"

        __str__ = __repr__

    class MyUnion(IdlUnion, metaclass=MyUnionMeta):
        __class__ = name
        __name__ = name
        __qualname__ = name
        _discriminator = discriminator
        _cases = cases
        _default = default_
        _default_val = _union_default_finder(discriminator, cases) if default_ else None
        _field_set = field_set
        _is_key = key

    from .main import IDL, proto_deserialize, proto_serialize
    IDL(MyUnion)
    MyUnion.serialize = proto_serialize
    MyUnion.deserialize = classmethod(proto_deserialize)
    return MyUnion


def union(discriminator, key=False):
    def wraps(cls):
        type_info = get_type_hints(cls, include_extras=True)

        return make_union(cls.__qualname__, discriminator, type_info, key=key)
    return wraps