# tests/test_assignments_02.py
import ast
import inspect
import itertools as it
import textwrap
import pytest

from fp_learning import assignments_02 as A_02


# -------------------------
# AST helpers (docstring-safe)
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

def _defines_methods_on_class(cls, *names: str) -> bool:
    d = cls.__dict__
    return all(name in d and callable(d[name]) for name in names)


# -------------------------
# 기능 테스트
# -------------------------
def test_countdown_basic_and_protocol():
    c = A_02.Countdown(3)
    assert list(c) == [3, 2, 1]

    it_obj = iter(A_02.Countdown(2))
    assert next(it_obj) == 2
    assert next(it_obj) == 1
    with pytest.raises(StopIteration):
        next(it_obj)

def test_countdown_zero_negative():
    assert list(A_02.Countdown(0)) == []
    assert list(A_02.Countdown(-5)) == []

def test_batched_basic_exact_and_partial():
    assert list(A_02.batched([1, 2, 3, 4], 2)) == [(1, 2), (3, 4)]
    assert list(A_02.batched([1, 2, 3, 4, 5], 2)) == [(1, 2), (3, 4), (5,)]

def test_batched_tuple_and_iterator_input():
    src_iter = iter([10, 11, 12])
    out = list(A_02.batched(src_iter, 2))
    assert out == [(10, 11), (12,)]
    assert all(isinstance(b, tuple) for b in out)

def test_batched_invalid_k():
    with pytest.raises(ValueError):
        list(A_02.batched([1, 2, 3], 0))
    with pytest.raises(ValueError):
        list(A_02.batched([1, 2, 3], -1))

def test_batched_with_infinite_safe():
    stream = it.count(1)
    first3 = list(it.islice(A_02.batched(stream, 4), 3))
    assert first3 == [(1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12)]

def test_take_drop_finite():
    data = [0, 1, 2, 3, 4]
    assert list(A_02.take(3, data)) == [0, 1, 2]
    assert list(A_02.drop(3, data)) == [3, 4]
    assert list(A_02.take(0, data)) == []
    assert list(A_02.drop(0, data)) == [0, 1, 2, 3, 4]

def test_take_drop_iterators_and_infinite():
    stream = it.count(10)
    assert list(A_02.take(5, stream)) == [10, 11, 12, 13, 14]
    assert list(A_02.take(3, stream)) == [15, 16, 17]

    stream2 = it.count(0)
    dropped = A_02.drop(100, stream2)
    assert list(it.islice(dropped, 5)) == [100, 101, 102, 103, 104]


# -------------------------
# 스타일 테스트 (AST 기반, docstring/주석 무시)
# -------------------------
def test_style_countdown_protocol_and_no_yield_or_list():
    assert _defines_methods_on_class(A_02.Countdown, "__iter__", "__next__"), \
        "Countdown은 __iter__/__next__를 직접 구현해야 합니다."
    t = _ast_of(A_02.Countdown)
    assert not _has_yield(t), "Countdown은 제너레이터(yield) 대신 클래스 기반으로 구현하세요."
    assert not _uses_call_name(t, "list"), "Countdown에서 list(materialize) 금지"

def test_style_batched_is_lazy_no_list():
    t = _ast_of(A_02.batched)
    assert not _uses_call_name(t, "list"), "batched에서 list(materialize) 금지"
    # 지연 수단: yield 또는 islice 사용을 권장
    assert _has_yield(t) or _uses_call_name(t, "islice"), \
        "batched는 yield 또는 itertools.islice 등 지연 수단을 사용해야 합니다."

def test_style_take_drop_are_lazy():
    for fn in (A_02.take, A_02.drop):
        t = _ast_of(fn)
        assert not _uses_call_name(t, "list"), f"{fn.__name__}에서 list(materialize) 금지"
        assert _has_yield(t) or _uses_call_name(t, "islice"), \
            f"{fn.__name__}는 yield 또는 itertools.islice 등 지연 수단을 사용해야 합니다."
