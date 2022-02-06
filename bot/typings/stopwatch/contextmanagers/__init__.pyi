from typing import NamedTuple


class Caller(NamedTuple):
    module: str
    function: str
    line_number: int
    ...


def inspect_caller(offset: int = ...) -> Caller:
    ...


def format_elapsed_time(elapsed: float) -> str:
    """
    Format the elapsed time in seconds to a human readable string.

    Parameters
    ----------
    elapsed : `float`
        The elapsed time in seconds.

    Returns
    -------
    `str`
        The formatted elapsed time.
    """
    ...
