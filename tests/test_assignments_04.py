# path: test_assignments_04.py
import ast
import inspect
import itertools as it
import textwrap
import pytest

from fp_learning import assignments_04 as A_04


# -------------------------
# AST helpers (docstring/주석 무시)
# -------------------------
def _ast_of(obj):
    src = textwrap.dedent(inspect.getsource(obj))
    return ast.parse(src)

def _uses_call_name(tree: ast.AST, name: str) -> bool:
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name) and f.id == name:
                return True
            if isinstance(f, ast.Attribute) and f.attr == name:
                return True
    return False

def _has_node_types(tree: ast.AST, types) -> bool:
    return any(isinstance(n, types) for n in ast.walk(tree))

def _has_yield(tree: ast.AST) -> bool:
    return _has_node_types(tree, (ast.Yield, ast.YieldFrom))


# -------------------------
# 기능 테스트W
# -------------------------
def test_compose2_numeric_and_text():
    try:
        f = lambda b: b * 2
        g = lambda a: a + 3
        h = A_04.compose2(f, g)  # h(x) == f(g(x)) == (x+3)*2
        assert h(4) == 14

        str_hex = A_04.compose2(str, hex)  # int -> hex(str)
        assert str_hex(31) == "0x1f"
    except NotImplementedError:
        pytest.skip("compose2 not implemented yet")

def test_compose2_has_type_hints():
    sig = inspect.signature(A_04.compose2)
    assert "f" in sig.parameters and "g" in sig.parameters
    assert sig.return_annotation is not inspect._empty


def test_pipe_iter_with_infinite_source_is_lazy():
    def evens(it_):
        for x in it_:
            if x % 2 == 0:
                yield x 

    def times3(it_):
        for x in it_:
            yield x * 3

    try:
        out = list(it.islice(A_04.pipe_iter(it.count(1), evens, times3), 5))
    except NotImplementedError:
        pytest.skip("pipe_iter not implemented yet")
    assert out == [6, 12, 18, 24, 30]

def test_pipe_iter_string_normalization():
    def normalize(it_):
        for s in it_:
            t = " ".join(str(s).strip().lower().split())
            if t:
                yield t

    data = ["  Hello ", " WORLD", "", "PyThOn  "]
    try:
        out_iter = A_04.pipe_iter(data, normalize)
    except NotImplementedError:
        pytest.skip("pipe_iter not implemented yet")
    assert list(out_iter) == ["hello", "world", "python"]

def test_pipe_iter_returns_iterable_not_materialized():
    def id_stage(it_):
        for x in it_:
            yield x

    try:
        it_out = A_04.pipe_iter([1, 2, 3], id_stage)
    except NotImplementedError:
        pytest.skip("pipe_iter not implemented yet")
    assert hasattr(it_out, "__iter__") and not isinstance(it_out, list)
    assert list(it_out) == [1, 2, 3]


def test_discounted_total_for_books_basic():
    items = [
        {"name": "A", "price": 10000.0, "qty": 2, "category": "book"},  # 포함
        {"name": "B", "price": 5000.0, "qty": 1, "category": "book"},   # qty<2 → 제외
        {"name": "C", "price": 20000.0, "qty": 3, "category": "toy"},   # book 아님 → 제외
        {"name": "D", "price": 1999.0, "qty": 2, "category": "book"},   # 포함
    ]
    try:
        got = A_04.discounted_total_for_books(items)
    except NotImplementedError:
        pytest.skip("discounted_total_for_books not implemented yet")
    assert got == 21598.2  # (10000*2 + 1999*2) * 0.9 -> 21598.2

def test_discounted_total_for_books_rounding_and_empty():
    try:
        got1 = A_04.discounted_total_for_books([{"name":"E","price":19.99,"qty":3,"category":"book"}])
        got2 = A_04.discounted_total_for_books([])
    except NotImplementedError:
        pytest.skip("discounted_total_for_books not implemented yet")
    assert got1 == 53.97
    assert got2 == 0.0


# -------------------------
# 스타일 테스트 (AST 기반)
# -------------------------
def test_style_compose2_no_for_or_try():
    t = _ast_of(A_04.compose2)
    assert not _has_node_types(t, ast.For), "compose2: 명시적 for 금지 (람다/중첩함수로 합성하세요)."
    assert not _has_node_types(t, ast.Try), "compose2: 불필요한 예외 처리 금지."

def test_style_pipe_iter_is_lazy_and_no_list():
    t = _ast_of(A_04.pipe_iter)
    assert _has_yield(t) or _uses_call_name(t, "islice"), "pipe_iter: yield 또는 itertools.islice 등 지연 수단 사용"
    assert not _uses_call_name(t, "list"), "pipe_iter: list(materialize) 금지"

def test_style_discounted_total_no_explicit_for_no_list():
    t = _ast_of(A_04.discounted_total_for_books)
    assert not _has_node_types(t, ast.For), "discounted_total_for_books: 명시적 for 금지 (컴프리헨션/내장 활용)"
    assert not _uses_call_name(t, "list"), "discounted_total_for_books: list(materialize) 금지"
