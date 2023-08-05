# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2020 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Integer type."""

from .._plum import Plum, getbytes
from ._inttype import IntType
from ._intview import IntView


class Int(int, Plum, metaclass=IntType):

    """Interpret bytes as an integer.

    :param x: value
    :type x: number or str
    :param int base: base of x when x is ``str``

    """

    __byteorder__ = 'little'
    __dref__ = None
    __max__ = 0xffffffff
    __min__ = 0
    __nbytes__ = 4
    __signed__ = False
    __strict_enum__ = False
    __enum__ = False

    def __init__(self, x=0, base=10):  # pylint: disable=super-init-not-called
        # pylint: disable=unused-argument
        if not self.__min__ <= self <= self.__max__:
            raise ValueError(
                f'{type(self).__name__} requires '
                f'{self.__min__} <= number <= {self.__max__}')

    @classmethod
    def _add_flags_to_dump(cls, value, dump):
        pass

    @classmethod
    def __unpack__(cls, buffer, offset, parent, dump):
        chunk, offset = getbytes(buffer, offset, cls.__nbytes__, dump, cls)

        self = int.from_bytes(chunk, cls.__byteorder__, signed=cls.__signed__)

        if dump:
            dump.value = self
            cls._add_flags_to_dump(self, dump)

        return self, offset

    @classmethod
    def __pack__(cls, buffer, offset, parent, value, dump):
        nbytes = cls.__nbytes__

        if dump:
            dump.cls = cls
            dump.value = value

        # pylint: disable=unidiomatic-typecheck
        if cls.__enum__ and type(value) is not cls:
            try:
                value = cls(value)
            except ValueError:
                if cls.__strict_enum__:
                    raise
            else:
                if dump:
                    dump.value = value
        # pylint: enable=unidiomatic-typecheck

        try:
            to_bytes = value.to_bytes
        except AttributeError:
            if dump:
                # in case str or some other type that looks like an int when
                # converted to str
                dump.value = repr(value)
            raise TypeError(
                f'value type {type(value)!r} not int-like '
                f'(no to_bytes() method)')

        chunk = to_bytes(nbytes, cls.__byteorder__, signed=cls.__signed__)

        if dump:
            dump.memory = chunk
            cls._add_flags_to_dump(value, dump)

        end = offset + nbytes
        buffer[offset:end] = chunk

        return end

    @classmethod
    def __view__(cls, buffer, offset=0):
        """Create plum view of bytes buffer.

        :param buffer: bytes buffer
        :type buffer: bytes-like (e.g. bytes, bytearray, memoryview)
        :param int offset: byte offset

        """
        return IntView(cls, buffer, offset)

    def __repr__(self):
        return f'{type(self).__name__}({int(self)})'
