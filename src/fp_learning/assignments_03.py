# path: fp_learning/assignments_03.py
from __future__ import annotations

from dataclasses import dataclass
from re import L
from typing import Callable, Generic, Iterable, Iterator, List, Sequence, TypeVar

T = TypeVar("T")
U = TypeVar("U")


# -----------------------------
# Helper: Maybe / Just / Nothing
# (과제의 초점은 아래 함수들에 있습니다.
#  Maybe는 이미 구현되어 있으며 수정할 필요 없습니다.)
# -----------------------------
class Maybe(Generic[T]):
    def map(self, f: Callable[[T], U]) -> "Maybe[U]":
        raise NotImplementedError
    def flatmap(self, f: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        raise NotImplementedError
    def get_or(self, default: U | T) -> U | T:
        raise NotImplementedError

@dataclass(frozen=True)
class Just(Maybe[T]):
    value: T
    def map(self, f: Callable[[T], U]) -> "Maybe[U]":
        try:
            return Just(f(self.value))
        except Exception:
            return Nothing()
    def flatmap(self, f: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        try:
            return f(self.value)
        except Exception:
            return Nothing()
    def get_or(self, default: U | T) -> U | T:
        return self.value
    def __repr__(self) -> str:
        return f"Just({self.value!r})"

class Nothing(Maybe[T]):
    def map(self, f: Callable[[T], U]) -> "Maybe[U]":
        return self  # 그대로 Nothing
    def flatmap(self, f: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        return self
    def get_or(self, default: U | T) -> U | T:
        return default
    def __repr__(self) -> str:
        return "Nothing()"

def maybe(x: T | None) -> Maybe[T]:
    return Nothing() if x is None else Just(x)


# -----------------------------
# Assignment 1: lazy_flatmap
# -----------------------------
def lazy_flatmap(fn: Callable[[T], Iterable[U]], xs: Iterable[T]) -> Iterator[U]:
    """제너레이터로 **지연(flat)** 평탄화한다.

    조건
    - 반드시 **제너레이터(yield / yield from)** 로 구현 (inspect.isgeneratorfunction 통과)
    - **list(materialize) 금지**
    - 무한 이터러블과도 안전: (예) islice로 앞 일부만 평가 가능
    - fn은 각 원소를 iterable로 변환한다고 가정 (예: list, tuple, generator 등)
    """
    for x in xs:
        for y in fn(x):
            yield y
            


# -----------------------------
# Assignment 2: safe_get_in
# -----------------------------
def safe_get_in(d: dict, path: Sequence[str]) -> Maybe[object]:
    """딕셔너리에서 경로를 안전하게 따라가 값을 가져온다.

    조건
    - **사각괄호 인덱싱( d[k] ) 금지**, 반드시 dict.get 사용
    - 경로 중 하나라도 없으면 **Nothing**을 반환
    - 정상 접근 시 **Just(value)** 반환
    - 재귀/반복 방식 자유
    예)
      user = {'profile': {'email': 'a@b.com'}}
      safe_get_in(user, ['profile', 'email']) -> Just('a@b.com')
      safe_get_in(user, ['profile', 'phone']) -> Nothing()
    """
    for path_item in path:
        value = d.get(path_item)
        if value:
            d = value
        else:
            return Nothing()
    return Just(d)
    
    


# -----------------------------
# Assignment 3: process_numbers_pipeline
# -----------------------------
def to_int_or_none(s: str) -> Maybe[int]:
    try:
        return Just(int(s))
    except Exception:
        return Nothing()

def keep_if(pred: Callable):
    return lambda x: Just(x) if pred(x) else Nothing()

def process_numbers_pipeline(strings: Iterable[str]) -> List[int]:
    """문자열 리스트에서 정수 파싱 → 짝수 필터 → 제곱 → 100 이상만.

    조건
    - **명시적 for문(ast.For) 금지** — 컴프리헨션 또는 map/filter 조합 권장
    - 예외 처리(try/except)는 이 함수 내부에서 사용하지 말고, 제공된 **to_int_or_none**을 사용
    - 반환은 List[int]
    예)
      ['10','-','20','x','7'] -> [100, 400]
    """
    stream = (
        to_int_or_none(s)                             # Maybe[int]
          .flatmap(keep_if(lambda n: (n & 1) == 0))   # 짝수만
          .map(lambda n: n * n)                       # 제곱
          .flatmap(keep_if(lambda n: n >= 100))       # 100 이상만
          .get_or(None)                               # Optional[int]
        for s in strings
    )
    return [v for v in stream if v is not None]