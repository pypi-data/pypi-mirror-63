from collections import deque
from functools import wraps
from inspect import BoundArguments
from inspect import signature
from typing import Any
from typing import Callable
from typing import Dict
from typing import Hashable
from typing import NamedTuple
from typing import Optional
from typing import Type
from typing import TypeVar


DEFAULT_MAXSIZE = 128
_T = TypeVar("_T")


class _HashableBoundArguments:
    """A hashable representation of BoundArguments."""

    def __init__(
        self: "_HashableBoundArguments", bound_args: BoundArguments,
    ) -> None:
        self._bound_args = bound_args

    def __eq__(self: "_HashableBoundArguments", other: Any) -> bool:
        return (
            hash(self) == hash(other)
            if isinstance(other, _HashableBoundArguments)
            else NotImplemented
        )

    def __hash__(self: "_HashableBoundArguments") -> int:
        return hash(
            (self._bound_args.args, tuple(self._bound_args.kwargs.items())),
        )


class _Cache:
    """A dict with max-sizing via a deque."""

    def __init__(
        self: "_Cache", *, maxsize: Optional[int] = DEFAULT_MAXSIZE,
    ) -> None:
        self._dict = {}
        self._deque = deque(maxlen=maxsize)
        self._hits = self._misses = 0
        self._maxsize = maxsize

    def __len__(self: "_Cache") -> int:
        return len(self._dict)

    def __repr__(self: "_Cache") -> str:
        return repr((self._dict, self._deque))

    __str__ = __repr__

    def __getitem__(self: "_Cache", key: Hashable) -> Any:
        try:
            value = self._dict[key]
        except KeyError:
            self._misses += 1
            raise
        else:
            self._hits += 1
            self._deque.remove(key)
            self._deque.append(key)
            return value

    def __setitem__(self: "_Cache", key: Hashable, value: Any) -> None:
        self._dict[key] = value
        try:
            self._deque.index(key)
        except ValueError:
            try:
                first = self._deque[0]
            except IndexError:
                self._deque.append(key)
            else:
                self._deque.append(key)
                if self._deque[0] != first:
                    del self._dict[first]

    @property
    def info(self: "_Cache") -> "CacheInfo":
        return CacheInfo(
            hits=self._hits,
            misses=self._misses,
            maxsize=self._maxsize,
            currsize=len(self),
        )

    def clear(self: "_Cache") -> None:
        self._dict.clear()
        self._deque.clear()
        self._hits = self._misses = 0


class CacheInfo(NamedTuple):
    """A set of summary statistics on the cache."""

    hits: int
    misses: int
    maxsize: int
    currsize: int


def hashable_lru_cache(
    *,
    maxsize: Optional[int] = DEFAULT_MAXSIZE,
    transforms: Optional[Dict[Type, Callable[..., Hashable]]] = None,
) -> Callable[[Callable[..., _T]], Callable[..., Callable[..., _T]]]:
    """An extension of functools.lru_cache allowing unhashable objects to be
    transformed and used in the cache key.

    maxsize:    the maximum size of the cache if int; unbounded if None
    transforms: a mapping of the form {type: func} where `func` is expected to
                transform objects of `type` into hashable versions
    """

    def apply_transforms(x: Any) -> Any:
        if transforms is None:
            return x
        else:
            try:
                func = next(
                    v for k, v in transforms.items() if isinstance(x, k)
                )
            except StopIteration:
                return x
            else:
                return func(x)

    def decorator(func: Callable[..., _T]) -> Callable[..., Callable[..., _T]]:
        sig = signature(func)
        cache = _Cache(maxsize=maxsize)

        @wraps(func)
        def decorated_func(*args: Any, **kwargs: Any) -> Callable[..., _T]:
            key = _HashableBoundArguments(
                sig.bind(
                    *map(apply_transforms, args),
                    **{k: apply_transforms(v) for k, v in kwargs.items()},
                ),
            )
            try:
                return cache[key]
            except KeyError:
                value = cache[key] = func(*args, **kwargs)
                return value

        def cache_info() -> "CacheInfo":
            return cache.info

        def cache_clear() -> None:
            cache.clear()

        decorated_func._cache = cache
        decorated_func.cache_info = cache_info
        decorated_func.cache_clear = cache_clear

        return decorated_func

    return decorator
