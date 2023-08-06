from operator import neg
from typing import Set

from hypothesis import given
from hypothesis.strategies import integers

from functional_itertools.classes import CFrozenSet
from tests.test_utilities import small_lists


# multiprocessing


@given(x=small_lists(integers()).map(set))
def test_pmap(x: Set[int]) -> None:
    y = CFrozenSet(x).pmap(neg)
    assert isinstance(y, CFrozenSet)
    assert y == set(map(neg, x))
