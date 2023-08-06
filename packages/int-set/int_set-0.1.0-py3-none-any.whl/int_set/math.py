import math as m
from functools import reduce


def cached_method(store):
    def decorator(func):
        def run(*args):
            key = tuple(sorted(args[1:]))
            if key in store:
                return store[key]
            store[key] = func(*args)
            return store[key]

        return run

    return decorator


class Cache:
    def __init__(self):
        self.gcd = {}
        self.lcm = {}


cache = Cache()


class Math:
    def __init__(self):
        self.cached_gcd = {}
        self.cached_lcm = {}

    @cached_method(cache.gcd)
    def _gcd(self, a, b):
        return m.gcd(a, b)

    @cached_method(cache.lcm)
    def _lcm(self, a, b):
        return (a * b) // self._gcd(a, b)

    @cached_method(cache.gcd)
    def gcd(self, *nums):
        return reduce(self._gcd, nums)

    @cached_method(cache.lcm)
    def lcm(self, *nums):
        return reduce(self._lcm, nums, 1)


math = Math()
