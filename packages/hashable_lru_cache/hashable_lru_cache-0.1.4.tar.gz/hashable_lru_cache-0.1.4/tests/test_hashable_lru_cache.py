import datetime as dt
from functools import lru_cache
from time import sleep
from typing import Iterable
from typing import NamedTuple

from pytest import raises

from hashable_lru_cache import hashable_lru_cache
from hashable_lru_cache.hashable_lru_cache import CacheInfo
from hashable_lru_cache.hashable_lru_cache import DEFAULT_MAXSIZE


def test_hashable_lru_cache() -> None:
    class Result(NamedTuple):
        time: dt.datetime
        length: int

    @lru_cache()
    def lru_func(x: Iterable) -> Result:
        return Result(dt.datetime.utcnow(), len(x))

    assert isinstance(lru_func(range(3)), Result)

    x = [1, 2, 3]
    with raises(TypeError, match="unhashable type"):
        lru_func(x)

    @hashable_lru_cache(transforms={list: tuple})
    def hashable_lru_func(x: Iterable) -> Result:
        sleep(0.1)
        return Result(dt.datetime.utcnow(), len(x))

    # initial
    assert hashable_lru_func.cache_info() == CacheInfo(0, 0, DEFAULT_MAXSIZE, 0)

    # first computation
    result = hashable_lru_func([1, 2, 3])
    assert hashable_lru_func.cache_info() == CacheInfo(0, 1, DEFAULT_MAXSIZE, 1)

    # first hit
    assert hashable_lru_func([1, 2, 3]) == Result(result.time, 3)
    assert hashable_lru_func.cache_info() == CacheInfo(1, 1, DEFAULT_MAXSIZE, 1)

    # second hit
    hashable_lru_func([1, 2, 3])
    assert hashable_lru_func.cache_info() == CacheInfo(2, 1, DEFAULT_MAXSIZE, 1)

    # third hit -- tuples equivalent
    hashable_lru_func((1, 2, 3))
    assert hashable_lru_func.cache_info() == CacheInfo(3, 1, DEFAULT_MAXSIZE, 1)

    # second computation
    hashable_lru_func([1, 2, 3, 4])
    assert hashable_lru_func.cache_info() == CacheInfo(3, 2, DEFAULT_MAXSIZE, 2)

    # clear
    hashable_lru_func.cache_clear()
    assert hashable_lru_func.cache_info() == CacheInfo(0, 0, DEFAULT_MAXSIZE, 0)
