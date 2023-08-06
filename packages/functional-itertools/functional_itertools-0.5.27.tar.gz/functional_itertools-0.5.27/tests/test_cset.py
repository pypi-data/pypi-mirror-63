from itertools import chain
from itertools import permutations
from operator import neg
from re import search
from typing import List
from typing import Set
from typing import Tuple
from typing import Type
from typing import Union

from hypothesis import assume
from hypothesis import given
from hypothesis import infer
from hypothesis import settings
from hypothesis.strategies import booleans
from hypothesis.strategies import integers
from hypothesis.strategies import just
from hypothesis.strategies import sampled_from
from hypothesis.strategies import sets
from hypothesis.strategies import tuples
from pytest import raises

from functional_itertools import CDict
from functional_itertools.classes import CFrozenSet
from functional_itertools.classes import CSet
from functional_itertools.utilities import drop_sentinel
from functional_itertools.utilities import Sentinel
from functional_itertools.utilities import sentinel
from tests.test_utilities import small_ints
from tests.test_utilities import small_lists


# repr and str


@given(x=sets(integers()))
def test_repr(x: Set[int]) -> None:
    y = repr(CSet(x))
    if x:
        assert search(r"^CSet\(\{[\d\s\-,]*\}\)$", y)
    else:
        assert y == "CSet()"


@given(x=sets(integers()))
def test_str(x: Set[int]) -> None:
    y = str(CSet(x))
    if x:
        assert search(r"^CSet\(\{[\d\s\-,]*\}\)$", y)
    else:
        assert y == "CSet()"


# built-ins


@given(x=sets(booleans()))
def test_all(x: Set[bool]) -> None:
    y = CSet(x).all()
    assert isinstance(y, bool)
    assert y == all(x)


@given(x=sets(booleans()))
def test_any(x: Set[bool]) -> None:
    y = CSet(x).any()
    assert isinstance(y, bool)
    assert y == any(x)


@given(x=sets(tuples(integers(), integers())))
def test_dict(x: Set[Tuple[int, int]]) -> None:
    y = CSet(x).dict()
    assert isinstance(y, CDict)
    assert all(isinstance(k, int) for k in y.keys())
    assert all(isinstance(v, int) for v in y.values())


@given(x=sets(integers()), start=integers())
def test_enumerate(x: Set[int], start: int) -> None:
    assert isinstance(CSet(x).enumerate(start=start), CSet)


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
    x = CSet.range(start, *args)
    assert isinstance(x, CSet)
    assert x == set(range(start, *args))


classes = sampled_from([CSet, CFrozenSet])
CSetOrCFrozenset = Union[Type[CSet], Type[CFrozenSet]]


@given(cls=classes, x=infer, xs=infer)
def test_union(cls: CSetOrCFrozenset, x: Set[int], xs: List[Set[int]]) -> None:
    y = cls(x).union(*xs)
    assert isinstance(y, cls)
    assert y == x.union(*xs)


@given(cls=classes, x=infer, xs=infer)
def test_intersection(
    cls: CSetOrCFrozenset, x: Set[int], xs: List[Set[int]],
) -> None:
    y = cls(x).intersection(*xs)
    assert isinstance(y, cls)
    assert y == x.intersection(*xs)


@given(cls=classes, x=infer, xs=infer)
def test_difference(
    cls: CSetOrCFrozenset, x: Set[int], xs: List[Set[int]],
) -> None:
    y = cls(x).difference(*xs)
    assert isinstance(y, cls)
    assert y == x.difference(*xs)


@given(cls=classes, x=infer, y=infer)
def test_symmetric_difference(
    cls: CSetOrCFrozenset, x: Set[int], y: Set[int],
) -> None:
    z = cls(x).symmetric_difference(y)
    assert isinstance(z, cls)
    assert z == x.symmetric_difference(y)


@given(cls=classes, x=infer)
def test_copy(cls: CSetOrCFrozenset, x: Set[int]) -> None:
    y = cls(x).copy()
    assert isinstance(y, cls)
    assert y == x


@given(x=infer)
def test_update(x: Set[int]) -> None:
    with raises(
        RuntimeError, match="Use the 'union' method instead of 'update'",
    ):
        CSet(x).update()


@given(x=infer)
def test_intersection_update(x: Set[int]) -> None:
    with raises(
        RuntimeError,
        match="Use the 'intersection' method instead of 'intersection_update'",
    ):
        CSet(x).intersection_update()


@given(x=infer)
def test_difference_update(x: Set[int]) -> None:
    with raises(
        RuntimeError,
        match="Use the 'difference' method instead of 'difference_update'",
    ):
        CSet(x).difference_update()


@given(x=infer)
def test_symmetric_difference_update(x: Set[int]) -> None:
    with raises(
        RuntimeError,
        match="Use the 'symmetric_difference' method "
        "instead of 'symmetric_difference_update'",
    ):
        CSet(x).symmetric_difference_update()


@given(x=infer, y=infer)
def test_add(x: Set[int], y: int) -> None:
    cset = CSet(x).add(y)
    assert isinstance(cset, CSet)
    assert cset == set(chain(x, [y]))


@given(x=infer, y=infer)
def test_remove(x: Set[int], y: int) -> None:
    cset = CSet(x)
    if y in x:
        new = cset.remove(y)
        assert isinstance(new, CSet)
        assert new == {i for i in x if i != y}
    else:
        with raises(KeyError, match=str(y)):
            cset.remove(y)


@given(x=infer, y=infer)
def test_discard(x: Set[int], y: int) -> None:
    cset = CSet(x).discard(y)
    assert isinstance(cset, CSet)
    assert cset == {i for i in x if i != y}


@given(x=infer)
def test_pop(x: Set[int]) -> None:
    cset = CSet(x)
    if cset:
        new = cset.pop()
        assert isinstance(new, CSet)
        assert len(new) == (len(x) - 1)
    else:
        with raises(KeyError, match="pop from an empty set"):
            cset.pop()


# multiprocessing


@given(x=small_lists(integers()).map(set))
@settings(deadline=None)
def test_pmap(x: Set[int]) -> None:
    y = CSet(x).pmap(neg, processes=1)
    assert isinstance(y, CSet)
    assert y == set(map(neg, x))


# extra public


@given(x=sets(integers()))
def test_pipe(x: Set[int]) -> None:
    y = CSet(x).pipe(permutations, r=2)
    assert isinstance(y, CSet)
    assert y == set(permutations(x, r=2))
