from itertools import accumulate
from itertools import chain
from itertools import compress
from itertools import dropwhile
from itertools import filterfalse
from itertools import groupby
from itertools import repeat
from re import escape
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

from hypothesis import given
from hypothesis.strategies import booleans
from hypothesis.strategies import fixed_dictionaries
from hypothesis.strategies import integers
from hypothesis.strategies import just
from hypothesis.strategies import lists
from hypothesis.strategies import none
from hypothesis.strategies import sets
from hypothesis.strategies import tuples
from pytest import mark
from pytest import raises
from pytest import warns

from functional_itertools import CFrozenSet
from functional_itertools import CIterable
from functional_itertools import CSet
from functional_itertools.classes import CDict
from functional_itertools.classes import CList
from functional_itertools.utilities import drop_sentinel
from functional_itertools.utilities import Sentinel
from functional_itertools.utilities import sentinel
from functional_itertools.utilities import VERSION
from functional_itertools.utilities import Version
from tests.test_utilities import int_and_int_to_int_funcs
from tests.test_utilities import int_to_bool_funcs
from tests.test_utilities import int_to_int_funcs
from tests.test_utilities import small_ints
from tests.test_utilities import small_lists


# built-ins


@given(x=sets(booleans()))
def test_all(x: Set[bool]) -> None:
    y = CList(x).all()
    assert isinstance(y, bool)
    assert y == all(x)


@given(x=sets(booleans()))
def test_any(x: Set[bool]) -> None:
    y = CList(x).any()
    assert isinstance(y, bool)
    assert y == any(x)


@given(x=lists(tuples(integers(), integers())))
def test_dict(x: List[Tuple[int, int]]) -> None:
    y = CList(x).dict()
    assert isinstance(y, CDict)
    assert all(isinstance(k, int) for k in y.keys())
    assert all(isinstance(v, int) for v in y.values())


@given(x=lists(integers()), start=integers())
def test_enumerate(x: List[int], start: int) -> None:
    y = CList(x).enumerate(start=start)
    assert isinstance(y, CList)
    assert y == list(enumerate(x, start=start))


@given(x=lists(integers()), func=int_to_bool_funcs)
def test_filter(x: List[int], func: Callable[[int], bool]) -> None:
    y = CList(x).filter(func)
    assert isinstance(y, CList)
    assert y == list(filter(func, x))


@given(x=sets(integers()))
def test_frozenset(x: Set[int]) -> None:
    y = CList(x).frozenset()
    assert isinstance(y, CFrozenSet)
    assert y == x


@given(x=lists(integers()))
def test_iter(x: List[int]) -> None:
    y = CList(x).iter()
    assert isinstance(y, CIterable)
    assert list(y) == x


@given(x=lists(integers()))
def test_list(x: List[int]) -> None:
    y = CList(x).list()
    assert isinstance(y, CList)
    assert y == x


@given(x=lists(integers()), func=int_to_bool_funcs)
def test_map(x: List[int], func: Callable[[int], bool]) -> None:
    y = CList(x).map(func)
    assert isinstance(y, CList)
    assert y == list(map(func, x))


@given(
    x=sets(integers()),
    key_kwargs=just({})
    | fixed_dictionaries(
        {
            "key": (
                int_to_int_funcs
                if VERSION in {Version.py36, Version.py37}
                else (none() | int_to_int_funcs)
            ),
        },
    ),
    default_kwargs=just({}) | fixed_dictionaries({"default": integers()}),
)
@mark.parametrize("func", [max, min])
def test_max_and_min(
    x: Set[int],
    func: Callable[..., int],
    key_kwargs: Dict[str, int],
    default_kwargs: Dict[str, int],
) -> None:
    try:
        y = getattr(CList(x), func.__name__)(**key_kwargs, **default_kwargs)
    except ValueError:
        with raises(
            ValueError,
            match=escape(f"{func.__name__}() arg is an empty sequence"),
        ):
            func(x, **key_kwargs, **default_kwargs)
    else:
        assert isinstance(y, int)
        assert y == func(x, **key_kwargs, **default_kwargs)


@given(x=lists(integers()))
def test_reversed(x: List[int]) -> None:
    y = CList(x).reversed()
    assert isinstance(y, CList)
    assert y == list(reversed(x))


@given(x=sets(integers()))
def test_set(x: Set[int]) -> None:
    y = CList(x).set()
    assert isinstance(y, CSet)
    assert y == x


@given(x=lists(integers()), key=none() | int_to_int_funcs, reverse=booleans())
def test_sort(
    x: List[int], key: Optional[Callable[[int], int]], reverse: bool,
) -> None:
    with warns(UserWarning, match="Use the 'sorted' method instead of 'sort'"):
        y = CList(x).sort(key=key, reverse=reverse)
    assert isinstance(y, CList)
    assert y == sorted(x, key=key, reverse=reverse)


@given(x=lists(integers()), key=none() | int_to_int_funcs, reverse=booleans())
def test_sorted(
    x: List[int], key: Optional[Callable[[int], int]], reverse: bool,
) -> None:
    y = CList(x).sorted(key=key, reverse=reverse)
    assert isinstance(y, CList)
    assert y == sorted(x, key=key, reverse=reverse)


@given(x=lists(integers()), start=integers() | just(sentinel))
def test_sum(x: List[int], start: Union[int, Sentinel]) -> None:
    y = CList(x).sum(start=start)
    assert isinstance(y, int)
    args, _ = drop_sentinel(start)
    assert y == sum(x, *args)


@given(x=lists(integers()))
def test_tuple(x: List[int]) -> None:
    y = CList(x).tuple()
    assert isinstance(y, tuple)
    assert y == tuple(x)


@given(
    x=lists(integers()), iterables=small_lists(lists(integers())),
)
def test_zip(x: List[int], iterables: List[List[int]]) -> None:
    y = CList(x).zip(*iterables)
    assert isinstance(y, CList)
    assert y == list(zip(x, *iterables))


# itertools


@given(x=integers(), times=small_ints)
def test_repeat(x: int, times: int) -> None:
    y = CList.repeat(x, times=times)
    assert isinstance(y, CList)
    assert y == list(repeat(x, times=times))


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
