"""Python collections in a functional-programming style."""
from functional_itertools.classes import CDict
from functional_itertools.classes import CFrozenSet
from functional_itertools.classes import CIterable
from functional_itertools.classes import CList
from functional_itertools.classes import CSet
from functional_itertools.errors import EmptyIterableError
from functional_itertools.errors import MultipleElementsError


__version__ = "0.5.23"
_ = {
    CDict,
    CFrozenSet,
    CIterable,
    CList,
    CSet,
    EmptyIterableError,
    MultipleElementsError,
}
