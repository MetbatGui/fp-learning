# path: tests/test_assignments_03.py
import ast
import inspect
import itertools as it
import textwrap
import pytest

from fp_learning import assignments_03 as A_03


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

def _has_subscript(tree: ast.AST) -> bool:
    # 전체 트리에서 Subscript 존재 여부 (서명/타입힌트까지 포함)
    return _has_node_types(tree, ast.Subscript)

def _has_try(tree: ast.AST) -> bool:
    return _has_node_types(tree, ast.Try)

def _has_runtime_subscript(func_obj) -> bool:
    """
    함수 '본문(body)' 내부에서만 Subscript(d[k]) 사용을 검사.
    시그니처(type annotation의 Sequence[str] 등)은 제외한다.
    """
    src = textwrap.dedent(inspect.getsource(func_obj))
    mod = ast.parse(src)
    fn = next((n for n in mod.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))), None)
    if fn is None:
        return False
    body_mod = ast.Module(body=fn.body, type_ignores=[])
    for n in ast.walk(body_mod):
        if isinstance(n, ast.Subscript):
            return True
    return False


# -------------------------
# 기능 테스트
# -------------------------
@pytest.mark.parametrize(
    "data, fn, expected",
    [
        ([[1], [2, 3], []], lambda x: x, [1, 2, 3]),
        ([[], [0], [10]], lambda x: x, [0, 10]),
        ([[1, 2], [3]], lambda xs: (n for n in xs if n % 2 == 1), [1, 3]),
    ],
)
def test_lazy_flatmap_basic(data, fn, expected):
    # 미구현 시 NotImplementedError를 정상적으로 전달
    try:
        out_iter = A_03.lazy_flatmap(fn, data)
    except NotImplementedError:
        pytest.skip("lazy_flatmap not implemented yet")
    assert list(out_iter) == expected

def test_lazy_flatmap_is_lazy_and_generator():
    try:
        # 무한 이터러블에서 앞 일부만 안전히 가져올 수 있어야 함
        stream = it.count(0)
        it5 = A_03.lazy_flatmap(lambda n: [n], stream)
    except NotImplementedError:
        pytest.skip("lazy_flatmap not implemented yet")
    # 제너레이터 함수인지 (yield 사용)
    assert inspect.isgeneratorfunction(A_03.lazy_flatmap), "lazy_flatmap은 제너레이터(yield)로 구현하세요."
    # 앞 5개만 슬라이스
    first5 = list(it.islice(it5, 5))
    assert first5 == [0, 1, 2, 3, 4]

def test_safe_get_in_works_with_present_and_missing():
    d = {'a': {'b': {'c': 42}}}
    try:
        j = A_03.safe_get_in(d, ['a', 'b', 'c'])
        n = A_03.safe_get_in(d, ['a', 'x'])
    except NotImplementedError:
        pytest.skip("safe_get_in not implemented yet")
    assert isinstance(j, A_03.Just), "safe_get_in: 값이 있으면 Just 반환"
    assert j.get_or(None) == 42
    assert isinstance(n, A_03.Nothing), "safe_get_in: 없으면 Nothing 반환"
    assert n.get_or("missing") == "missing"

@pytest.mark.parametrize(
    "strings, expected",
    [
        (['10','-','20','x','7'], [100, 400]),
        (['50','3','-2','oops','0'], [2500]),
        ([], []),
    ],
)
def test_process_numbers_pipeline(strings, expected):
    try:
        out = A_03.process_numbers_pipeline(strings)
    except NotImplementedError:
        pytest.skip("process_numbers_pipeline not implemented yet")
    assert out == expected


# -------------------------
# 스타일 테스트 (AST 기반)
# -------------------------
def test_style_lazy_flatmap_generator_and_no_list():
    t = _ast_of(A_03.lazy_flatmap)
    assert _has_yield(t), "lazy_flatmap: yield 또는 yield from 을 사용하세요."
    assert not _uses_call_name(t, "list"), "lazy_flatmap: list(materialize) 금지"

def test_style_safe_get_in_uses_get_and_no_subscript():
    t = _ast_of(A_03.safe_get_in)
    assert _uses_call_name(t, "get"), "safe_get_in: dict.get을 사용하세요."
    # 함수 '본문' 내부에서만 d[k] 금지 검사 (타입힌트의 []는 허용)
    assert not _has_runtime_subscript(A_03.safe_get_in), "safe_get_in: d[k] 형태의 사각괄호 인덱싱 금지"

def test_style_process_numbers_pipeline_prefers_comprehensions_no_try():
    t = _ast_of(A_03.process_numbers_pipeline)
    # 명시적 for문 금지 (컴프리헨션은 허용; ast.For만 금지)
    assert not _has_node_types(t, ast.For), "process_numbers_pipeline: 명시적 for 문 금지 (컴프리헨션 사용)"
    # 내부 예외 처리 금지
    assert not _has_try(t), "process_numbers_pipeline: try/except 대신 to_int_or_none를 사용하세요."
    # 헬퍼 사용 권장
    assert _uses_call_name(t, "to_int_or_none"), "process_numbers_pipeline: to_int_or_none를 사용하세요."
