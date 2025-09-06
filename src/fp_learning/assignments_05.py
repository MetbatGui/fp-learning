# path: fp_learning/assignments_05.py
from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from typing import Callable, Generic, Iterable, TypeVar, Union

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")
A = TypeVar("A")
B = TypeVar("B")


# -----------------------------
# Minimal containers (self-contained for the assignment)
# -----------------------------
@dataclass(frozen=True, slots=True)
class Just(Generic[T]):
    value: T
    def __repr__(self) -> str:
        return f"Just({self.value!r})"

class Nothing(Generic[T]):
    __slots__ = ()
    def __repr__(self) -> str:
        return "Nothing"

Maybe = Union[Just[T], Nothing[T]]

@dataclass(frozen=True, slots=True)
class Ok(Generic[T]):
    value: T
    def __repr__(self) -> str:
        return f"Ok({self.value!r})"

@dataclass(frozen=True, slots=True)
class Err(Generic[E]):
    error: E
    def __repr__(self) -> str:
        return f"Err({self.error!r})"

Result = Union[Ok[T], Err[E]]

def ok(v: T) -> Ok[T]: return Ok(v)
def err(e: E) -> Err[E]: return Err(e)

def is_ok(r: Result[T, E]) -> bool: return isinstance(r, Ok)
def is_err(r: Result[T, E]) -> bool: return isinstance(r, Err)


# -----------------------------
# Assignment 1: Result.apply (Applicative 스타일)
# -----------------------------
def result_apply(val: Result[T, E], rf: Result[Callable[[T], U], E]) -> Result[U, E]:
    """`Result` 안의 함수를 `Result` 안의 값에 적용한다.

    요구사항
    - 둘 중 하나라도 Err면 Err를 반환 (오른쪽 rf가 Err면 그 Err, 아니면 val의 Err).
    - 둘 다 Ok면 rf.value(val.value)를 Ok로 감싼다.
    - 명시적 for-loop 금지.
    """
    if isinstance(rf, Err):
        return rf
    if isinstance(val, Err):
        return val
    
    return ok(rf.value(val.value))
    

# -----------------------------
# Assignment 2: Maybe <-> Result 변환
# -----------------------------
def maybe_to_result(m: Maybe[T], error: E) -> Result[T, E]:
    """`Just(v)` -> `Ok(v)`, `Nothing` -> `Err(error)`.
    명시적 for-loop 금지."""
    if isinstance(m, Just):
        return ok(m.value)
    if isinstance(m, Nothing):
        return err(error)

def result_to_maybe(r: Result[T, E]) -> Maybe[T]:
    """`Ok(v)` -> `Just(v)`, `Err(e)` -> `Nothing`.
    명시적 for-loop 금지."""
    if is_ok(r):
        return Just(r.value)
    if is_err(r):
        return Nothing()


# -----------------------------
# Assignment 3: Result.sequence / Result.traverse
# -----------------------------
def result_sequence(xs: Iterable[Result[T, E]]) -> Result[list[T], E]:
    """Iterable[Result[T,E]] -> Result[List[T],E]

    요구사항
    - 왼쪽→오른쪽으로 접으면서, 하나라도 Err면 **즉시** 그 Err를 반환.
    - 모두 Ok면 내부 값을 리스트로 모아 Ok(List[T]) 반환.
    - 명시적 for-loop(ast.For) 금지 (reduce, comprehension 등 허용).
    """
    it = iter(xs)
    acc: list[T] = []
    while True:
        try:
            r = next(it)
        except StopIteration:
            return ok(acc)
        if is_err(r):
            return r
        acc.append(r.value)

def result_traverse(xs: Iterable[A], f: Callable[[A], Result[B, E]]) -> Result[list[B], E]:
    """Iterable[A]와 함수 f: A->Result[B,E]를 받아 Result[List[B],E]를 반환.

    요구사항
    - `map(f, xs)` 후 `result_sequence`로 처리하거나, 동일 동작을 직접 구현.
    - 명시적 for-loop(ast.For) 금지.
    """
    it = iter(xs)
    acc: list[B] = []
    while True:
        try:
            x = next(it)
        except StopIteration:
            return ok(acc)
        r = f(x)
        if is_err(r):
            return r
        acc.append(r.value)