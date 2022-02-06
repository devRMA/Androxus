from typing import List, Optional

class Statistics:
    _values: List[float]

    def __init__(self, values: Optional[List[float]] = ...) -> None:
        ...

    def add(self, value: float) -> None:
        """
        Add a new value in seconds to get the statistics.

        Parameters
        ----------
        value : `float`
            The value to add in seconds.
        """
        ...

    @property
    def mean(self) -> float:
        """`float`: Return the mean value in seconds."""
        ...

    @property
    def maximum(self) -> float:
        """`float`: Return the maximum value in seconds."""
        ...

    @property
    def median(self) -> float:
        """`float`: Return the median value in seconds."""
        ...

    @property
    def minimum(self) -> float:
        """`float`: Return the minimum value in seconds."""
        ...

    @property
    def total(self) -> float:
        """`float`: Return the total value in seconds."""
        ...

    @property
    def variance(self) -> float:
        """`float`: Return the variance in seconds."""
        ...

    def __len__(self) -> int:
        ...
