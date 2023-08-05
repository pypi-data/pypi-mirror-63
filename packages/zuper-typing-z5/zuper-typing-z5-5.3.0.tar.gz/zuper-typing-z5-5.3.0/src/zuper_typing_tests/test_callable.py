from dataclasses import dataclass
from typing import Callable

from nose.tools import assert_equal

# from zuper_ipce_tests.test_utils import assert_type_roundtrip
from zuper_typing.annotations_tricks import get_Callable_info, is_Callable
from zuper_typing.monkey_patching_typing import MyNamedArg as NamedArg


def test_detection_1():
    T = Callable[[], int]
    # print(T.__dict__)
    assert is_Callable(T)

    res = get_Callable_info(T)
    assert_equal(res.parameters_by_name, {})
    assert_equal(res.parameters_by_position, ())
    assert_equal(res.returns, int)


def test_detection_2():
    T = Callable[[NamedArg(str, "A")], int]

    assert is_Callable(T)

    res = get_Callable_info(T)
    assert_equal(res.returns, int)
    assert_equal(res.parameters_by_position, (str,))
    assert_equal(res.parameters_by_name, {"A": str})


def test_detection_3():
    T = Callable[[NamedArg(str, "A")], int]

    assert is_Callable(T)

    res = get_Callable_info(T)
    assert_equal(res.returns, int)
    assert_equal(res.parameters_by_position, (str,))
    assert_equal(res.parameters_by_name, {"A": str})


def test_detection_4():
    @dataclass
    class MyClass:
        pass

    T = Callable[[NamedArg(MyClass, "A")], int]

    assert is_Callable(T)

    res = get_Callable_info(T)
    assert_equal(res.returns, int)
    assert_equal(res.parameters_by_position, (MyClass,))
    assert_equal(res.parameters_by_name, {"A": MyClass})


def test_NamedArg_eq():
    a = NamedArg(int, "A")
    b = NamedArg(int, "A")

    assert_equal(a, b)

    A = Callable[[NamedArg(int, "A")], int]
    B = Callable[[NamedArg(int, "A")], int]

    assert_equal(A, B)


# @raises(TypeError)


def test_back():
    T = Callable[[NamedArg(str, "A")], int]

    assert is_Callable(T)

    res = get_Callable_info(T)
    T2 = res.as_callable()
