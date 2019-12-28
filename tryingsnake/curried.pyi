import tryingsnake
from typing import Callable, TypeVar

T = TypeVar("T")

def Try(f: Callable[..., T]) -> Callable[..., tryingsnake.Try_[T]]: ...
