import inspect
import types
import pytest

from fp_learning import assignments_01 as A_01

@pytest.mark.parametrize(
    "inp, outp",
    [
        ([1, 2, 3, 4, 5], [1, 8, 27, 64, 125]),
        ([0, -1, 2], [0, -1, 8]),
    ],
)
def test_assignment1_values(inp, outp):
    assert A_01.assignment1(inp) == outp

@pytest.mark.parametrize(
    "inp, outp",
    [
        (["Python", "Functional", "Programming"], [6, 10, 11]),
        (["", "ab"], [0, 2]),
    ],
)
def test_assignment2_values(inp, outp):
    assert A_01.assignment2(inp) == outp

@pytest.mark.parametrize(
    "inp, outp",
    [
        ([10, 20, 30, 40], [5.0, 10.0, 15.0, 20.0]),
        ([1, 3], [0.5, 1.5]),
    ],
)
def test_assignment3_values(inp, outp):
    assert A_01.assignment3(inp) == outp

# ---- 선택: 구현 스타일 가벼운 규칙 검사 ----
def _assert_uses_map_and_no_for(fn: types.FunctionType):
    src = inspect.getsource(fn)
    # 아주 가벼운 규칙: 'map('은 포함, 'for '는 금지
    assert "map(" in src, f"{fn.__name__} must use map"
    assert "for " not in src, f"{fn.__name__} must not use for-loop"

def test_style_constraints():
    _assert_uses_map_and_no_for(A_01.assignment1)
    _assert_uses_map_and_no_for(A_01.assignment2)
    _assert_uses_map_and_no_for(A_01.assignment3)
