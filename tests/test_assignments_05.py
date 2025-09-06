# path: tests/test_assignments_05.py
import ast
import inspect
import textwrap
import pytest

from fp_learning import assignments_05 as A_05


# -------------------------
# AST helpers (docstring/주석 무시)
# -------------------------
def _ast_of(obj):
    src = textwrap.dedent(inspect.getsource(obj))
    return ast.parse(src)

def _has_node_types(tree, *node_types):
    return any(isinstance(n, node_types) for n in ast.walk(tree))

def _uses_call_name(tree, name: str) -> bool:
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            if isinstance(n.func, ast.Name) and n.func.id == name:
                return True
            if isinstance(n.func, ast.Attribute) and n.func.attr == name:
                return True
    return False


# -------------------------
# Value tests
# -------------------------
def test_apply_ok_ok():
    rf = A_05.ok(lambda x: x + 1)
    v  = A_05.ok(3)
    try:
        out = A_05.result_apply(v, rf)
    except NotImplementedError:
        pytest.skip("result_apply not implemented yet")
    assert isinstance(out, A_05.Ok) and out.value == 4

def test_apply_err_on_function():
    rf = A_05.err("E1")
    v  = A_05.ok(3)
    try:
        out = A_05.result_apply(v, rf)
    except NotImplementedError:
        pytest.skip("result_apply not implemented yet")
    assert isinstance(out, A_05.Err) and out.error == "E1"

def test_apply_err_on_value():
    rf = A_05.ok(lambda x: x * 2)
    v  = A_05.err("bad")
    try:
        out = A_05.result_apply(v, rf)
    except NotImplementedError:
        pytest.skip("result_apply not implemented yet")
    assert isinstance(out, A_05.Err) and out.error == "bad"


def test_maybe_result_bridge():
    j = A_05.Just(10)
    n = A_05.Nothing()
    try:
        assert A_05.maybe_to_result(j, "no") == A_05.ok(10)
        assert A_05.maybe_to_result(n, "err!") == A_05.err("err!")
        assert A_05.result_to_maybe(A_05.ok(42)).__repr__().startswith("Just(")
        assert isinstance(A_05.result_to_maybe(A_05.err("x")), A_05.Nothing)
    except NotImplementedError:
        pytest.skip("maybe_to_result/result_to_maybe not implemented yet")


def test_sequence_and_traverse_values():
    def parse_int(s: str) -> A_05.Result[int, str]:
        try:
            return A_05.ok(int(s))
        except ValueError:
            return A_05.err(f"'{s}'")

    try:
        # sequence
        assert A_05.result_sequence([A_05.ok(1), A_05.ok(2)]) == A_05.ok([1, 2])
        assert isinstance(A_05.result_sequence([A_05.ok(1), A_05.err("boom"), A_05.ok(3)]), A_05.Err)

        # traverse
        data_good = ["1", "2", "3"]
        data_bad  = ["1", "x", "3"]
        out = A_05.result_traverse(data_good, parse_int)
        assert out == A_05.ok([1, 2, 3])
        out2 = A_05.result_traverse(data_bad, parse_int)
        assert isinstance(out2, A_05.Err)
    except NotImplementedError:
        pytest.skip("result_sequence/result_traverse not implemented yet")


# -------------------------
# Style tests
# -------------------------
def test_style_no_explicit_for_in_sequence_and_traverse():
    for fn in (A_05.result_sequence, A_05.result_traverse):
        t = _ast_of(fn)
        assert not _has_node_types(t, ast.For), f"{fn.__name__}: 명시적 for 금지 (reduce/map/컴프리헨션 권장)"

def test_style_apply_no_for():
    t = _ast_of(A_05.result_apply)
    assert not _has_node_types(t, ast.For), "result_apply: 명시적 for 금지"
