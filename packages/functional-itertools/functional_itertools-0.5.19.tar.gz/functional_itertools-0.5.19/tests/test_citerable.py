from functools import reduce
from itertools import accumulate
from itertools import chain
from itertools import combinations
from itertools import combinations_with_replacement
from itertools import compress
from itertools import count
from itertools import cycle
from itertools import dropwhile
from itertools import filterfalse
from itertools import groupby
from itertools import islice
from itertools import permutations
from itertools import product
from itertools import repeat
from itertools import starmap
from itertools import takewhile
from itertools import tee
from itertools import zip_longest
from pathlib import Path
from re import escape
from string import ascii_lowercase
from sys import maxsize
from tempfile import TemporaryDirectory
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import NoReturn
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

from hypothesis import assume
from hypothesis import given
from hypothesis.strategies import booleans
from hypothesis.strategies import data
from hypothesis.strategies import DataObject
from hypothesis.strategies import fixed_dictionaries
from hypothesis.strategies import floats
from hypothesis.strategies import integers
from hypothesis.strategies import iterables
from hypothesis.strategies import just
from hypothesis.strategies import lists
from hypothesis.strategies import none
from hypothesis.strategies import sets
from hypothesis.strategies import text
from hypothesis.strategies import tuples
from more_itertools import chunked
from more_itertools import flatten
from pytest import mark
from pytest import raises

from functional_itertools.classes import CFrozenSet
from functional_itertools.classes import CIterable
from functional_itertools.classes import CList
from functional_itertools.classes import CSet
from functional_itertools.errors import EmptyIterableError
from functional_itertools.errors import MultipleElementsError
from functional_itertools.utilities import drop_sentinel
from functional_itertools.utilities import Sentinel
from functional_itertools.utilities import sentinel
from functional_itertools.utilities import VERSION
from functional_itertools.utilities import Version
from tests.test_utilities import assert_is_instance_and_equal_to
from tests.test_utilities import int_and_int_to_int_funcs
from tests.test_utilities import int_to_bool_funcs
from tests.test_utilities import int_to_int_funcs


lengths = integers(0, 1000)


@given(x=integers() | lists(integers()))
def test_init(x: Union[int, List[int]]) -> None:
    if isinstance(x, int):
        with raises(
            TypeError,
            match="CIterable expected an iterable, "
            "but 'int' object is not iterable",
        ):
            CIterable(x)  # type: ignore
    else:
        assert isinstance(CIterable(iter(x)), CIterable)


@given(x=lists(integers()), index=integers() | floats())
def test_get_item(x: List[int], index: Union[int, float]) -> None:
    y = CIterable(x)
    if isinstance(index, int):
        num_ints = len(x)
        if index < 0:
            with raises(
                IndexError, match=f"Expected a non-negative index; got {index}",
            ):
                y[index]
        elif 0 <= index < num_ints:
            assert_is_instance_and_equal_to(y[index], int, x[index])
        elif num_ints <= index <= maxsize:
            with raises(IndexError, match="CIterable index out of range"):
                y[index]
        else:
            with raises(
                IndexError,
                match=f"Expected an index at most {maxsize}; got {index}",
            ):
                y[index]
    else:
        with raises(
            TypeError, match=escape("Expected an int or slice; got a(n) float"),
        ):
            y[index]


@given(x=lists(integers()))
def test_dunder_iter(x: List[int]) -> None:
    assert list(CIterable(x)) == x


# repr and str


@given(x=iterables(integers()))
def test_repr(x: Iterable[int]) -> None:
    assert repr(CIterable(x)) == f"CIterable({x!r})"


@given(x=iterables(integers()))
def test_str(x: Iterable[int]) -> None:
    assert str(CIterable(x)) == f"CIterable({x})"


# built-ins


@given(x=sets(booleans()))
def test_all(x: Set[bool]) -> None:
    y = CIterable(x).all()
    assert isinstance(y, bool)
    assert y == all(x)


@given(x=sets(booleans()))
def test_any(x: Set[bool]) -> None:
    y = CIterable(x).any()
    assert isinstance(y, bool)
    assert y == any(x)


@given(x=lists(tuples(text(alphabet=ascii_lowercase), integers())))
def test_dict(x: List[Tuple[str, int]]) -> None:
    y = CIterable(x).dict()
    assert isinstance(y, dict)
    assert all(isinstance(k, str) for k in y.keys())
    assert all(isinstance(v, int) for v in y.values())


@given(x=lists(integers()), start=integers())
def test_enumerate(x: List[int], start: int) -> None:
    y = CIterable(x).enumerate(start=start)
    assert isinstance(y, CIterable)
    assert list(y) == list(enumerate(x, start=start))


@given(x=lists(integers()), func=int_to_bool_funcs)
def test_filter(x: List[int], func: Callable[[int], bool]) -> None:
    y = CIterable(x).filter(func)
    assert isinstance(y, CIterable)
    assert list(y) == list(filter(func, x))


@given(x=sets(integers()))
def test_frozenset(x: Set[int]) -> None:
    y = CIterable(x).frozenset()
    assert isinstance(y, CFrozenSet)
    assert y == x


@given(x=lists(integers()))
def test_iter(x: List[int]) -> None:
    y = CIterable(x).iter()
    assert isinstance(y, CIterable)
    assert list(y) == x


@given(x=lists(integers()))
def test_list(x: List[int]) -> None:
    y = CIterable(x).list()
    assert isinstance(y, CList)
    assert y == x


@given(x=lists(integers()), func=int_to_bool_funcs)
def test_map(x: List[int], func: Callable[[int], bool]) -> None:
    y = CIterable(x).map(func)
    assert isinstance(y, CIterable)
    assert list(y) == list(map(func, x))


@given(
    data=data(),
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
    data: DataObject,
    x: Set[int],
    func: Callable[..., int],
    key_kwargs: Dict[str, int],
    default_kwargs: Dict[str, int],
) -> None:
    try:
        y = getattr(CIterable(iter(x)), func.__name__)(
            **key_kwargs, **default_kwargs,
        )
    except ValueError:
        with raises(
            ValueError,
            match=escape(f"{func.__name__}() arg is an empty sequence"),
        ):
            func(x, **key_kwargs, **default_kwargs)
    else:
        assert isinstance(y, int)
        assert y == func(x, **key_kwargs, **default_kwargs)


@given(
    start=lengths, stop=lengths | just(sentinel), step=lengths | just(sentinel),
)
def test_range(
    start: int, stop: Union[int, Sentinel], step: Union[int, Sentinel],
) -> None:
    if step is sentinel:
        assume(stop is not sentinel)
    else:
        assume(step != 0)
    args, _ = drop_sentinel(stop, step)
    x = CIterable.range(start, *args)
    assert isinstance(x, CIterable)
    assert list(x) == list(range(start, *args))


@given(x=sets(integers()))
def test_set(x: Set[int]) -> None:
    y = CIterable(x).set()
    assert isinstance(y, CSet)
    assert y == x


@given(x=lists(integers()), key=none() | int_to_int_funcs, reverse=booleans())
def test_sorted(
    x: List[int], key: Optional[Callable[[int], int]], reverse: bool,
) -> None:
    y = CIterable(x).sorted(key=key, reverse=reverse)
    assert isinstance(y, CList)
    assert y == sorted(x, key=key, reverse=reverse)


@given(x=lists(integers()), start=integers() | just(sentinel))
def test_sum(x: List[int], start: Union[int, Sentinel]) -> None:
    y = CIterable(x).sum(start=start)
    assert isinstance(y, int)
    args, _ = drop_sentinel(start)
    assert y == sum(x, *args)


@given(x=lists(integers()))
def test_tuple(x: List[int]) -> None:
    y = CIterable(x).tuple()
    assert isinstance(y, tuple)
    assert y == tuple(x)


@given(x=lists(integers()), iterables=lists(lists(integers())), n=lengths)
def test_zip(x: List[int], iterables: List[List[int]], n: int) -> None:
    y = CIterable(x).zip(*iterables)
    assert isinstance(y, CIterable)
    assert list(y[:n]) == list(islice(zip(x, *iterables), n))


# public


@given(x=lists(integers()))
@mark.parametrize("method_name, index", [("first", 0), ("last", -1)])
def test_first_and_last(x: List[int], method_name: str, index: int) -> None:
    method = getattr(CIterable(x), method_name)
    if x:
        assert method() == x[index]
    else:
        with raises(EmptyIterableError):
            method()


@given(x=lists(integers()))
def test_one(x: List[int]) -> None:
    length = len(x)
    if length == 0:
        with raises(EmptyIterableError):
            CIterable(x).one()
    elif length == 1:
        assert CIterable(x).one() == x[0]
    else:
        with raises(MultipleElementsError, match=f"{x[0]}, {x[1]}"):
            CIterable(x).one()


@given(x=lists(integers()), n=integers(0, maxsize))
def test_pipe(x: List[int], n: int) -> None:
    y = CIterable(x).pipe(chunked, n)
    assert isinstance(y, CIterable)
    assert list(y) == list(chunked(x, n))


# functools


@given(
    x=lists(integers()),
    func=int_and_int_to_int_funcs,
    initial=integers() | just(sentinel),
)
def test_reduce(
    x: List[int],
    func: Callable[[int, int], int],
    initial: Union[int, Sentinel],
) -> None:
    args, _ = drop_sentinel(initial)
    try:
        y = CIterable(x).reduce(func, initial=initial)
    except EmptyIterableError:
        with raises(
            TypeError,
            match=escape("reduce() of empty sequence with no initial value"),
        ):
            reduce(func, x, *args)
    else:
        assert isinstance(y, int)
        assert y == reduce(func, x, *args)


@given(x=tuples(integers(), integers()))
def test_reduce_propagating_type_error(x: Tuple[int, int]) -> None:
    def func(*args: Any) -> NoReturn:
        raise TypeError("Always fail")

    with raises(TypeError, match="Always fail"):
        CIterable(x).reduce(func)


@mark.xfail
@given(
    x=lists(lists(integers())),
    initial=lists(integers()) | just(sentinel),
    n=lengths,
)
def test_reduce_as_iterable(
    x: List[List[int]], initial: Union[List[int], Sentinel], n: int,
) -> None:
    args, _ = drop_sentinel(initial)
    try:
        y = CIterable(x).reduce_as_iterable(
            lambda x, y: list(chain(x, y)), initial=initial,
        )
    except EmptyIterableError:
        assume(False)
    else:
        assert isinstance(y, CIterable)
        assert list(y[:n]) == list(islice(flatten(chain(x, args)), n))


# itertools


@given(
    start=integers(), step=integers(), n=lengths,
)
def test_count(start: int, step: int, n: int) -> None:
    x = CIterable.count(start=start, step=step)
    assert isinstance(x, CIterable)
    assert list(x[:n]) == list(islice(count(start=start, step=step), n))


@given(x=lists(integers()), n=lengths)
def test_cycle(x: List[int], n: int) -> None:
    y = CIterable(x).cycle()
    assert isinstance(y, CIterable)
    assert list(y[:n]) == list(islice(cycle(x), n))


@given(x=lists(integers()), times=integers(), n=lengths)
def test_repeat(x: int, times: int, n: int) -> None:
    try:
        y = CIterable.repeat(x, times=times)
    except OverflowError:
        assume(False)
    else:
        assert isinstance(y, CIterable)
        assert list(y[:n]) == list(islice(repeat(x, times=times), n))


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
    y = CIterable(x).accumulate(func, **initial_kwargs)
    assert isinstance(y, CIterable)
    assert list(y) == list(accumulate(x, func, **initial_kwargs))


@given(x=lists(integers()), xs=lists(lists(integers())), n=lengths)
def test_chain(x: List[int], xs: List[List[int]], n: int) -> None:
    y = CIterable(x).chain(*xs)
    assert isinstance(y, CIterable)
    assert list(y[:n]) == list(islice(chain(x, *xs), n))


@given(x=lists(integers()), selectors=lists(booleans()))
def test_compress(x: List[int], selectors: List[bool]) -> None:
    y = CIterable(x).compress(selectors)
    assert isinstance(y, CIterable)
    assert list(y) == list(compress(x, selectors))


@given(x=lists(integers()), func=int_to_bool_funcs)
def test_dropwhile(x: List[int], func: Callable[[int], bool]) -> None:
    y = CIterable(x).dropwhile(func)
    assert isinstance(y, CIterable)
    assert list(y) == list(dropwhile(func, x))


@given(x=lists(integers()), func=int_to_bool_funcs)
def test_filterfalse(x: List[int], func: Callable[[int], bool]) -> None:
    y = CIterable(x).filterfalse(func)
    assert isinstance(y, CIterable)
    assert list(y) == list(filterfalse(func, x))


@given(x=lists(integers()), key=none() | int_to_bool_funcs)
def test_groupby(x: List[int], key: Optional[Callable[[int], bool]]) -> None:
    y = CIterable(x).groupby(key=key)
    assert isinstance(y, CIterable)
    y = list(y)
    z = list(groupby(x, key=key))
    assert len(y) == len(z)
    for (key_y, group_y), (key_z, group_z) in zip(y, z):
        assert key_y == key_z
        assert list(group_y) == list(group_z)


@given(
    x=lists(integers()),
    start=lengths,
    stop=lengths | just(sentinel),
    step=lengths | just(sentinel),
)
def test_islice(
    x: List[int],
    start: int,
    stop: Union[int, Sentinel],
    step: Union[int, Sentinel],
) -> None:
    if step is sentinel:
        assume(stop is not sentinel)
    else:
        assume(step != 0)
    args, _ = drop_sentinel(stop, step)
    y = CIterable(x).islice(start, *args)
    assert isinstance(y, CIterable)
    assert list(y) == list(islice(x, start, *args))


@given(x=lists(tuples(integers(), integers())), func=int_and_int_to_int_funcs)
def test_starmap(
    x: List[Tuple[int, int]], func: Callable[[Tuple[int, int]], int],
) -> None:
    y = CIterable(x).starmap(func)
    assert isinstance(y, CIterable)
    assert list(y) == list(starmap(func, x))


@given(x=lists(integers()), func=int_to_bool_funcs)
def test_takewhile(x: List[int], func: Callable[[int], bool]) -> None:
    y = CIterable(x).takewhile(func)
    assert isinstance(y, CIterable)
    assert list(y) == list(takewhile(func, x))


@given(x=lists(integers()), n=lengths)
def test_tee(x: List[int], n: int) -> None:
    y = CIterable(x).tee(n=n)
    assert isinstance(y, CIterable)
    y = list(y)
    z = list(tee(x, n))
    assert len(y) == len(z)
    for y_i, z_i in zip(y, z):
        assert list(y_i) == list(z_i)


@given(
    x=lists(integers()),
    iterables=lists(lists(integers())),
    fillvalue=none() | integers(),
    n=lengths,
)
def test_zip_longest(
    x: List[int], iterables: List[List[int]], fillvalue: Optional[int], n: int,
) -> None:
    y = CIterable(x).zip_longest(*iterables, fillvalue=fillvalue)
    assert isinstance(y, CIterable)
    assert list(y[:n]) == list(
        islice(zip_longest(x, *iterables, fillvalue=fillvalue), n),
    )


@given(
    x=lists(integers()), iterables=lists(lists(integers())), n=lengths,
)
def test_product(x: List[int], iterables: List[List[int]], n: int) -> None:
    y = CIterable(x).product(*iterables)
    assert isinstance(y, CIterable)
    assert list(y[:n]) == list(islice(product(x, *iterables), n))


@given(
    x=lists(integers()), r=none() | lengths, n=lengths,
)
def test_permutations(x: List[int], r: Optional[int], n: int) -> None:
    y = CIterable(x).permutations(r=r)
    assert isinstance(y, CIterable)
    assert list(y[:n]) == list(islice(permutations(x, r=r), n))


@given(x=lists(integers()), r=lengths, n=lengths)
def test_combinations(x: List[int], r: int, n: int) -> None:
    y = CIterable(x).combinations(r)
    assert isinstance(y, CIterable)
    assert list(y[:n]) == list(islice(combinations(x, r), n))


@given(x=lists(integers()), r=lengths, n=lengths)
def test_combinations_with_replacement(x: List[int], r: int, n: int) -> None:
    y = CIterable(x).combinations_with_replacement(r)
    assert isinstance(y, CIterable)
    assert list(y[:n]) == list(islice(combinations_with_replacement(x, r), n))


# pathlib


@given(x=sets(text(alphabet=ascii_lowercase, min_size=1)), use_path=booleans())
def test_iterdir(x: Set[str], use_path: bool) -> None:
    with TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        for i in x:
            temp_dir.joinpath(i).touch()
        if use_path:
            y = CIterable.iterdir(temp_dir)
        else:
            y = CIterable.iterdir(temp_dir_str)
        assert isinstance(y, CIterable)
        assert y.set() == {temp_dir.joinpath(i) for i in x}
