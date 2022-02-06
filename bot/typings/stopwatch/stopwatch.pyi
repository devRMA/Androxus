from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator, List, Optional


class Lap:
    _running: bool
    _start: float
    _fractions: List[float]

    def __init__(self) -> None:
        ...

    def __repr__(self) -> str:
        ...

    @property
    def elapsed(self) -> float:
        """`float`: Return the elapsed time in seconds."""
        ...

    def start(self) -> None:
        """
        Start the lap timer.
        """
        ...

    def stop(self) -> None:
        """
        Stop the lap timer.
        """
        ...


class Stopwatch:
    _name: Optional[str]
    _laps: List[Lap]
    _lap: Optional[Lap]

    def __init__(self, name: Optional[str] = ...) -> None:
        ...

    def __enter__(self) -> Stopwatch:
        ...

    def __exit__(
        self, exc_type: Any, exc_value: Any, exc_traceback: Any
    ) -> None:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    @property
    def name(self) -> Optional[str]:
        """Optional[`str`]: The name of the stopwatch."""
        ...

    @property
    def laps(self) -> List[float]:
        """List[`float`]: The list of laps."""
        ...

    @property
    def elapsed(self) -> float:
        """`float`: The elapsed time in seconds."""
        ...

    @contextmanager
    def lap(self) -> Iterator[None]:
        """
        Context manager for add a new lap.
        """
        ...

    def start(self) -> Stopwatch:
        """
        Starts the stopwatch.

        Returns
        -------
        `Stopwatch`
            The started stopwatch instance.
        """
        ...

    def stop(self) -> Stopwatch:
        """
        Stops the stopwatch, freezing the duration.

        Returns
        -------
        `Stopwatch`
            The stopped stopwatch instance.
        """
        ...

    def reset(self) -> Stopwatch:
        """
        Resets the Stopwatch to 0 duration.

        Returns
        -------
        `Stopwatch`
            The resetted stopwatch instance.
        """
        ...

    def report(self) -> str:
        """
        Return a report of the stopwatch statistics.

        Returns
        -------
        `str`
            The report.
        """
        ...
