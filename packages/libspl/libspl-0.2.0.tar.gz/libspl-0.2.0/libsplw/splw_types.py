import typing


class SPLWString(str):
    """SPLW string. Python str but with SPLW string methods/properties"""

    @property
    def length(self):
        return len(self)


class SPLWList(list):
    """SPLW list. Python list but with SPLW list methods/properties"""

    @property
    def length(self):
        return len(self)


class SPLWComplex(complex):
    """SPLW complex. Python complex but with SPLW list methods/properties/comparison"""

    def __repr__(self):
        return f"({self.real}+{self.imag}i)"

    def __lt__(self, other):
        try:
            result = super() < other
        except TypeError:
            pass
        else:
            return result
        if isinstance(other, (float, int)):
            other = complex(other, 0)
        if isinstance(other, complex):
            if other.real != self.real:
                return self.real < other.real
            return self.imag < other.imag
        return NotImplemented

    def __le__(self, other):
        try:
            result = super() <= other
        except TypeError:
            pass
        else:
            return result
        if isinstance(other, (float, int)):
            other = complex(other, 0)
        if isinstance(other, complex):
            if other.real != self.real:
                return self.real < other.real
            return self.imag <= other.imag
        return NotImplemented

    def __gt__(self, other):
        try:
            result = super() > other
        except TypeError:
            pass
        else:
            return result
        if isinstance(other, (float, int)):
            other = complex(other, 0)
        if isinstance(other, complex):
            if other.real != self.real:
                return self.real > other.real
            return self.imag > other.imag
        return NotImplemented

    def __ge__(self, other):
        try:
            result = super() >= other
        except TypeError:
            pass
        else:
            return result
        if isinstance(other, (float, int)):
            other = complex(other, 0)
        if isinstance(other, complex):
            if other.real != self.real:
                return self.real > other.real
            return self.imag >= other.imag
        return NotImplemented


SPLWNumber = typing.Union[int, float, SPLWComplex]
SPLWType = typing.Union[SPLWNumber, SPLWList, bool, SPLWString, dict]

OBEYS_FLAGS = (int, float, SPLWComplex)
