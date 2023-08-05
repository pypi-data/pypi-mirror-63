from typing import Optional, Union

from nose.tools import raises

from zuper_typing.annotations_tricks import (
    get_Optional_arg,
    get_Union_args,
    is_Optional,
    is_Union,
    make_Union,
)
from zuper_typing.recursive_tricks import replace_typevars
from zuper_typing.uninhabited import make_Uninhabited


def test_making_union():
    make_Union(int)
    make_Union(int, float)
    make_Union(int, float, bool)
    make_Union(int, float, bool, str)
    make_Union(int, float, bool, str, bytes)
    make_Union(int, float, bool, str, bytes, int)


@raises(ValueError)
def test_corner_cases_empty_union():
    make_Union()


# @raises(ValueError)
def test_corner_cases_empty_union1():
    make_Union(int)


def test_multiple_optional():
    a = Union[int, str, type(None)]
    assert is_Optional(a), a
    U = get_Optional_arg(a)
    assert is_Union(U), U
    assert int, str == get_Union_args(U)


def test_multiple_optional2():
    ts = (int, str, type(None))
    a = make_Union(*ts)
    print(f"a = {a}")
    assert is_Optional(a), a
    U = get_Optional_arg(a)
    assert is_Union(U), U
    assert int, str == get_Union_args(U)


def test_multiple_optional3():
    ts = (int, type(None), str)
    a = make_Union(*ts)
    assert is_Optional(a), a
    U = get_Optional_arg(a)
    assert is_Union(U), U
    assert int, str == get_Union_args(U)


def test_optional1():
    T = Optional[int]
    S = get_Optional_arg(T)
    assert S is int


def test_multiple_union2():
    ts = (int, type(None))
    U = make_Union(*ts)
    assert is_Optional(U)


def test_unh():
    u = make_Uninhabited()
    replace_typevars(u, bindings={}, symbols={})


def test_union_simple():
    x = Union[int, str]
    assert is_Union(x)
