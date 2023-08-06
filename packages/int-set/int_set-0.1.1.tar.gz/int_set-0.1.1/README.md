# int set

# Abstract

Counts the number of integers.
整数を数えます。

## What does this do?

Counts the number of integers that can be any integer multiple within a given start and end.
始まりと終了を指定すると、その中に含まれる任意の整数倍となる整数の数を数えます。

Very Fast!!
## usage
```python
from int_set import IntSet, step

# IntSet makes range like object
# IntSetはrangeのようのオブジェクトを作成します。

_range = IntSet(100)       # start: 0 stop: 100
_range = IntSet(100, 1000) # start: 100 stop: 1000

s = step(2)   # a multiple of two（２の倍数）
s = step(2,5) # a multiple of 2 or a multiple of 5（２の倍数または５の倍数）

# Count multiples of 2 or 5 between 100 and 1000.
# 100 ~ 1000に含まれる２の倍数または５の倍数の数を数えます。
_range.count(s) # 541
```

## install

```shell script
pip install int-set
```