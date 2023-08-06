from int_set.step import Step


class IntSet:
    def __init__(self, stop: int, start: int = None):
        if start:
            start, stop = stop, start
        else:
            start = 0
        if not isinstance(start, int):
            raise TypeError(f"'{type(start)}' object cannot be interpreted as an integer")
        if not isinstance(stop, int):
            raise TypeError(f"'{type(stop)}' object cannot be interpreted as an integer")
        if stop < start:
            raise ValueError('stop cannot be less then start')
        self.stop = stop
        self.start = start

    def count(self, step: Step):
        length = 0
        plus, minus = step()
        for elm in plus:
            length += elm.len(self.start, self.stop)
        for elm in minus:
            length -= elm.len(self.start, self.stop)
        return length
