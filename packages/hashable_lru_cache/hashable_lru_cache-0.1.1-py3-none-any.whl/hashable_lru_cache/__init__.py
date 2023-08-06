"""An extension of functools.lru_cache allowing unhashable objects to be
transformed and used in the cache key."""
from hashable_lru_cache.hashable_lru_cache import hashable_lru_cache


__version__ = "0.1.1"
_ = {hashable_lru_cache}
