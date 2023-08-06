import operator
import functools

from int_set.step import Step, Element
from int_set.int_set import IntSet

__version__ = '0.1.0'


def step(step_, *steps):
    if len(steps) == 0:
        return Step(Element(step_))
    return Element(step_) + functools.reduce(operator.add, map(Element, steps))
