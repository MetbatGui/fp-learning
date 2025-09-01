# fp_learning/assignments_02.py
from __future__ import annotations

from collections.abc import Iterable, Iterator
import functools
from typing import TypeVar, Tuple

T = TypeVar("T")


class Countdown:
    """
    Countdown(n): n, n-1, ..., 1 을 지연 산출하는 커스텀 이터레이터.

    요구사항
    - n <= 0 이면 아무 것도 산출하지 않음.
    - iter/next 프로토콜을 직접 구현(__iter__/__next__).
    - list 등의 즉시(materialize) 변환 금지.
    """

    def __init__(self, n: int):
        if not isinstance(n, int):
            raise TypeError
        self.n = n

    def __iter__(self) -> "Countdown":
        return self

    def __next__(self) -> int:
        if self.n <= 0:
            raise StopIteration
        value = self.n
        self.n -= 1
        return value


def batched(iterable: Iterable[T], k: int) -> Iterator[Tuple[T, ...]]:
    """
    입력 이터러블을 길이 k의 '튜플'로 묶어 지연 산출한다.

    요구사항
    - 마지막 배치는 k보다 짧을 수 있음.
    - k <= 0 이면 ValueError.
    - 무한 이터러블(itertools.count 등)과도 안전하게 동작해야 함.
    - list(materialize) 금지. yield 또는 itertools 사용.
    """
    if k <= 0:
        raise ValueError
    it = iter(iterable)
    while True:
        batch = []
        for __ in range(k):
            try:
                batch.append(next(it))
            except StopIteration:
                if batch:
                    yield tuple(batch)
                return
        yield tuple(batch)
        


def take(n: int, it: Iterable[T]) -> Iterator[T]:
    """
    앞에서 n개만 지연 산출한다.

    요구사항
    - n <= 0 이면 아무 것도 산출하지 않음.
    - itertools.islice 또는 iter/next를 활용.
    - list(materialize) 금지.
    """
    if n <= 0:
        return

    it = iter(it)
    for __ in range(n):
        try:
            yield next(it)
        except StopIteration:
            return
        


def drop(n: int, it: Iterable[T]) -> Iterator[T]:
    """
    앞에서 n개를 건너뛴 나머지를 지연 산출한다.

    요구사항
    - n <= 0 이면 원본 전체 산출.
    - 무한 이터러블과 함께 사용해도 멈추지 않아야 함.
    - list(materialize) 금지.
    """
    k = 0
    it = iter(it)
    while True:
        try:
            value = next(it)
            if k >= n:
                yield value
            k += 1
        except StopIteration:
            return