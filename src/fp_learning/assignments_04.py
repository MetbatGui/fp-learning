# path: assignments_04.py
from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Any, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
T = TypeVar("T")
U = TypeVar("U")

__all__ = ["compose2", "pipe_iter", "discounted_total_for_books"]


def compose2(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    """
    타입 안전 2항 합성: compose2(f, g)(x) == f(g(x))

    예)
        h = compose2(str, hex)   # (int) -> str
        h(31) == "0x1f"

    규칙
    - 순수 함수만 합성한다(입력 불변, 외부 상태 변경 없음).
    - 타입 힌트를 정확히 유지할 것.
    """
    return lambda x: f(g(x))


def pipe_iter(
    data: Iterable[T],
    *stages: Callable[[Iterable[Any]], Iterable[Any]],
) -> Iterator[Any]:
    """
    이터러블 파이프라인(레이지 유지):
        pipe_iter(data, s1, s2, s3) == s3(s2(s1(data))) 를 '지연'으로 수행

    요구사항
    - 각 stage는 반드시 (Iterable[X]) -> Iterable[Y] 형태여야 함.
    - data/materialization을 하지 말 것(list(...) 금지).
    - 무한 이터러블에도 안전하게 동작해야 함(앞에서 일부만 소비 가능).

    힌트
    - 내부에서 현재 이터러블을 누적 갱신하며 마지막에 `yield from`으로 방출.
    """
    for stage in stages:
        data = stage(data)
    yield from data 


def discounted_total_for_books(items: Iterable[dict[str, Any]]) -> float:
    """
    미니 프로젝트:
    - 입력: {'name': str, 'price': float, 'qty': int, 'category': str} 시퀀스
    - 처리: (a) category == 'book' 필터
           (b) qty >= 2 필터
           (c) price * qty 누적 합
           (d) 10% 할인 적용
           (e) 소수점 둘째 자리 반올림 후 반환
    - 반환: float (예: 21598.2)

    규칙
    - 순수 함수로 작성(I/O 금지).
    - 입력 변경 금지(불변성).
    - 가능하면 파이프라인 스타일(내부 보조 함수 분리 권장).
    """

    is_book = lambda items: filter(lambda item:item.get('category') == 'book', items)
    is_qty_over_2 = lambda items: filter(lambda item:item.get('qty') >= 2, items)
    get_total = lambda items: sum((item.get('price') * item.get('qty') for item in items)) 
    apply_discount = lambda total: total * 0.9
    round_to_2 = lambda discounted_total: round(discounted_total, 2)

    books = is_book(items)
    qty_over_2s = is_qty_over_2(books)
    total = get_total(qty_over_2s)
    discounted_total = apply_discount(total)
    rounded_total = round_to_2(discounted_total)
    return rounded_total