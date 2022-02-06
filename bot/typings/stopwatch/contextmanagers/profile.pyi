from typing import Any, Callable, TypeVar

from ..statistics import Statistics
from . import Caller

RT = TypeVar('RT')


def make_report(caller: Caller, name: str, statistics: Statistics) -> str:
    """
    Return a report of the stopwatch statistics.

    Parameters
    ----------
    caller : `Caller`
        The caller.
    name : `str`
        The name for report.
    statistics : `Statistics`
        The statistics object.

    Returns
    -------
    `str`
        The report string.
    """
    ...


def print_report(caller: Caller, name: str, statistics: Statistics) -> None:
    """
    Print a report of the stopwatch statistics.

    Parameters
    ----------
    caller : `Caller`
        The caller.
    name : `str`
        The name for printing.
    statistics : `Statistics`
        The statistics object.
    """
    ...


def profile(**kwargs: Any) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    """
    Decorator for profiling the function.

    Parameters
    ----------
    name : Optional[`str`]
        The name for the statistics. Default is the name of function.
    report_every : Optional[`int`]
        The number of times to report the statistics. Default is 1.
    """
    ...
