from itertools import permutations
from operator import neg
from re import search
from typing import FrozenSet
from typing import Set
from typing import Union

from hypothesis import assume
from hypothesis import given
from hypothesis import infer
from hypothesis import settings
from hypothesis.strategies import integers
from hypothesis.strategies import just
from hypothesis.strategies import sets

from functional_itertools.classes import CFrozenSet
from functional_itertools.utilities import drop_sentinel
from functional_itertools.utilities import Sentinel
from functional_itertools.utilities import sentinel
from tests.test_utilities import small_ints
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


@given(
    start=small_ints,
    stop=small_ints | just(sentinel),
    step=small_ints | just(sentinel),
)
def test_range(
    start: int, stop: Union[int, Sentinel], step: Union[int, Sentinel],
) -> None:
    if step is sentinel:
        assume(stop is not sentinel)
    else:
        assume(step != 0)
    args, _ = drop_sentinel(stop, step)
    x = CFrozenSet.range(start, *args)
    assert isinstance(x, CFrozenSet)
    assert x == set(range(start, *args))


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
