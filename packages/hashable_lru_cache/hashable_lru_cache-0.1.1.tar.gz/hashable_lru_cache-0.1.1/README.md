# hashable_lru_cache
![PyPI](https://img.shields.io/pypi/v/hashable_lru_cache)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hashable_lru_cache)
[![Build Status](https://dev.azure.com/baoweiur521/baoweiur521/_apis/build/status/baowei521.hashable_lru_cache?branchName=master)](https://dev.azure.com/baoweiur521/baoweiur521/_build/latest?definitionId=5&branchName=master)

## Overview
`hashable_lru_cache` provides an extension of `functools.lru_cache` allowing unhashable objects to be transformed and used in the cache key.

## Examples

Suppose you wish a decorate a function accepting `list`s and `dict`s. Since these are unhashable, `functools.lru_cache` will not work here. Instead, we can use `hashable_lru_cache`, declaring all `list`s are to be cast into `tuple`s, and `dict`s are to be cast into `frozenset`s, which are now hashable.

```python
from hashable_lru_cache import hashable_lru_cache

@hashable_lru_cache(transforms={
    list: tuple,
    dict: (lambda x: frozenset(x.items()))},
)
def get_length(x):
    print(f"Calculating length for {x}...")
    return len(x)

# tests
get_length([1, 2, 3])  # Calculating length for [1, 2, 3]...
get_length([1, 2, 3])
get_length([1, 2, 4])  # Calculating length for [1, 2, 4]...
get_length(dict(a=1, b=2))  # Calculating length for {'a': 1, 'b': 2}...
get_length(dict(a=1, b=2))
get_length(dict(a=1, b=3))  # Calculating length for {'a': 1, 'b': 3}...
```

## Motivation

This was motivated by the need to hash `pandas.Series` and `pandas.DataFrames`. If you need this functionality, then you can check out [`hashable_ndframes`](https://github.com/baowei521/hashable_ndframes) and apply `transforms={Series: HashableSeries, DataFrame: HashableDataFrame}`.
