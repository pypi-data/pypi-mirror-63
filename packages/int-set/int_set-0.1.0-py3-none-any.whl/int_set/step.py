import itertools

from int_set.math import math


class Step:
    def __init__(self, *elm):
        self.elm = set(elm)

    def __str__(self):
        return f'{{{", ".join(map(str, self.elm))}}}'

    def __repr__(self):
        return f'Step({", ".join(map(str, self.elm))})'

    def lcm(self):
        return Element(math.lcm(*map(lambda x: x.data, self.elm)))

    def gcm(self):
        return Element(math.gcd(*map(lambda x: x.data, self.elm)))

    def add_element(self, element):
        if self.gcm().data % element.data == 0:
            return Step(element)
        rm = set()
        for elm in self.elm:
            if elm.data % element.data == 0:
                rm.add(elm)
            elif element.data % elm.data == 0:
                rm.add(element)
        return Step(*((self.elm | {element}) - rm))

    def add_set(self, set_):
        s = Step(*self.elm)
        for elm in set_.elm:
            s = s.add_element(elm)
        return s

    def __add__(self, other):
        if isinstance(other, Element):
            return self.add_element(other)
        if isinstance(other, Step):
            return self.add_set(other)
        raise TypeError(f'{type(other)} must be Element or Set')

    def __call__(self):
        plus = set()
        minus = set()
        for i in range(len(self.elm)):
            for s in map(lambda x: Step(*x), itertools.combinations(self.elm, i + 1)):
                if i % 2 == 0:
                    plus.add(s.lcm())
                else:
                    minus.add(s.lcm())
        return plus, minus


class Element:
    def __init__(self, n):
        self.data = n

    def __str__(self):
        return f'<{self.data}>'

    def __repr__(self):
        return f'Element({self.data})'

    def __eq__(self, other):
        return self.data == other.data

    def __hash__(self):
        return self.data

    def __add__(self, other):
        if isinstance(other, Element):
            small, large = (self, other) if self.data < other.data else (other, self)
            return Step(small) if large.data % small.data == 0 else Step(small, large)
        elif isinstance(other, Step):
            return other + self
        raise TypeError()

    def len(self, start, stop):
        if start % self.data == 0:
            return len(range(start, stop + 1, self.data))
        start = start + self.data - start % self.data
        return len(range(start, stop + 1, self.data))
