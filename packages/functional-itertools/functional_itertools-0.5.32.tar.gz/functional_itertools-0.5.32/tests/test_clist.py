from itertools import accumulate
from itertools import chain
from itertools import compress
from itertools import dropwhile
from itertools import filterfalse
from itertools import groupby
from itertools import permutations
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

from hypothesis import given
from hypothesis.strategies import booleans
from hypothesis.strategies import fixed_dictionaries
from hypothesis.strategies import integers
from hypothesis.strategies import just
from hypothesis.strategies import lists
from hypothesis.strategies import none
from pytest import mark
from pytest import warns

from functional_itertools.classes import CList
from functional_itertools.utilities import VERSION
from functional_itertools.utilities import Version
from tests.test_utilities import int_and_int_to_int_funcs
from tests.test_utilities import int_to_bool_funcs
from tests.test_utilities import int_to_int_funcs
from tests.test_utilities import small_lists


# built-ins


@given(x=lists(integers()))
def test_copy(x: List[int]) -> None:
    y = CList(x).copy()
    assert isinstance(y, CList)
    assert y == x


@given(x=lists(integers()))
def test_reversed(x: List[int]) -> None:
    y = CList(x).reversed()
    assert isinstance(y, CList)
    assert y == list(reversed(x))


@given(x=lists(integers()), key=none() | int_to_int_funcs, reverse=booleans())
def test_sort(
    x: List[int], key: Optional[Callable[[int], int]], reverse: bool,
) -> None:
    with warns(UserWarning, match="Use the 'sorted' method instead of 'sort'"):
        y = CList(x).sort(key=key, reverse=reverse)
    assert isinstance(y, CList)
    assert y == sorted(x, key=key, reverse=reverse)


# itertools


@given(
    x=lists(integers()),
    func=int_and_int_to_int_funcs,
    initial_kwargs=just({})
    if VERSION in {Version.py36, Version.py37}
    else fixed_dictionaries({"initial": none() | integers()}),
)
def test_accumulate(
    x: List[int],
    func: Callable[[int, int], int],
    initial_kwargs: Dict[str, Any],
) -> None:
    y = CList(x).accumulate(func, **initial_kwargs)
    assert isinstance(y, CList)
    assert y == list(accumulate(x, func, **initial_kwargs))


@given(
    x=small_lists(integers()), xs=small_lists(small_lists(integers())),
)
def test_chain(x: List[int], xs: List[List[int]]) -> None:
    y = CList(x).chain(*xs)
    assert isinstance(y, CList)
    assert y == list(chain(x, *xs))


@given(x=lists(integers()), selectors=lists(booleans()))
def test_compress(x: List[int], selectors: List[bool]) -> None:
    y = CList(x).compress(selectors)
    assert isinstance(y, CList)
    assert y == list(compress(x, selectors))


@given(x=lists(integers()), func=int_to_bool_funcs)
def test_dropwhile(x: List[int], func: Callable[[int], bool]) -> None:
    y = CList(x).dropwhile(func)
    assert isinstance(y, CList)
    assert y == list(dropwhile(func, x))


@given(x=lists(integers()), func=int_to_bool_funcs)
def test_filterfalse(x: List[int], func: Callable[[int], bool]) -> None:
    y = CList(x).filterfalse(func)
    assert isinstance(y, CList)
    assert y == list(filterfalse(func, x))


@mark.xfail
@given(x=lists(integers()), key=none() | int_to_bool_funcs)
def test_groupby(x: List[int], key: Optional[Callable[[int], bool]]) -> None:
    y = CList(x).groupby(key=key)
    assert isinstance(y, CList)
    z = list(groupby(x, key=key))
    assert len(y) == len(z)
    for (key_y, group_y), (key_z, group_z) in zip(y, z):
        assert key_y == key_z
        assert isinstance(group_y, CList)
        assert group_y == list(group_z)


# extra public


@given(x=lists(integers()))
def test_pipe(x: List[int]) -> None:
    y = CList(x).pipe(permutations, r=2)
    assert isinstance(y, CList)
    assert y == list(permutations(x, r=2))
