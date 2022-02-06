from typing import Any, Optional

from ..stopwatch import Stopwatch
from . import Caller


class stopwatch:
    _message: Optional[str]
    _caller: Caller
    _stopwatch: Stopwatch

    def __init__(self, message: Optional[str] = ...) -> None:
        ...

    def __enter__(self) -> None:
        ...

    def __exit__(
        self, exc_type: Any, exc_value: Any, exc_traceback: Any
    ) -> None:
        ...
