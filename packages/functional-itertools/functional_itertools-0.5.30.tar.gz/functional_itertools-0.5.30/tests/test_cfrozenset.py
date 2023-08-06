from itertools import permutations
from operator import neg
from re import search
from typing import FrozenSet
from typing import Set

from hypothesis import given
from hypothesis import infer
from hypothesis import settings
from hypothesis.strategies import integers
from hypothesis.strategies import sets

from functional_itertools.classes import CFrozenSet
from tests.test_utilities import small_lists


@given(x=infer)
def test_repr(x: FrozenSet[int]) -> None:
    y = repr(CFrozenSet(x))
    if x:
        assert search(r"^CFrozenSet\(\{[\d\s\-,]*\}\)$", y)
    else:
        assert y == "CFrozenSet()"


@given(x=infer)
def test_str(x: FrozenSet[int]) -> None:
    y = str(CFrozenSet(x))
    if x:
        assert search(r"^CFrozenSet\(\{[\d\s\-,]*\}\)$", y)
    else:
        assert y == "CFrozenSet()"


# built-in


# multiprocessing


@given(x=small_lists(integers()).map(set))
@settings(deadline=None)
def test_pmap(x: Set[int]) -> None:
    y = CFrozenSet(x).pmap(neg, processes=1)
    assert isinstance(y, CFrozenSet)
    assert y == set(map(neg, x))


# extra public


@given(x=sets(integers()))
def test_pipe(x: Set[int]) -> None:
    y = CFrozenSet(x).pipe(permutations, r=2)
    assert isinstance(y, CFrozenSet)
    assert y == set(permutations(x, r=2))
