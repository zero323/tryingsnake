from typing import (
    overload,
    Any,
    Callable,
    Generator,
    Generic,
    Iterable,
    Iterator,
    Optional,
    Tuple,
    Type,
    TypeVar,
)

T = TypeVar("T")
U = TypeVar("U")

class Try_(Generic[T]):
    _unhandled: Tuple[Exception, ...]
    @staticmethod
    def set_unhandled(es: Iterable[Exception] = ...) -> None: ...
    def __init__(self, _: Any) -> None: ...
    def __ne__(self, other: Any) -> bool: ...
    def get(self) -> T: ...
    def getOrElse(self, default: T) -> T: ...
    def orElse(self, default: Try_[T]) -> Try_[T]: ...
    def map(self, f: Callable[[T], U]) -> Try_[U]: ...
    def flatMap(self, f: Callable[[T], Try_[U]]) -> Try_[U]: ...
    def filter(
        self,
        f: Callable[[T], bool],
        exception_cls: Type[Exception] = ...,
        msg: Optional[str] = ...,
    ) -> Try_[T]: ...
    def recover(self, f: Callable[[Exception], T]) -> Try_[T]: ...
    def recoverWith(self, f: Callable[[Exception], Try_[T]]) -> Try_[T]: ...
    def failed(self) -> Try_[Exception]: ...
    @property
    def isFailure(self) -> bool: ...
    @property
    def isSuccess(self) -> bool: ...

class Success(Try_[T]):
    @staticmethod
    def __len__() -> int: ...
    def __init__(self, v: T): ...
    def __eq__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
    def get(self) -> T: ...
    def getOrElse(self, default: T) -> T: ...
    def orElse(self, default: Try_[T]) -> Try_[T]: ...
    def map(self, f: Callable[[T], U]) -> Try_[U]: ...
    def flatMap(self, f: Callable[[T], Try_[U]]) -> Try_[U]: ...
    def filter(
        self,
        f: Callable[[T], bool],
        exception_cls: Type[Exception] = ...,
        msg: Optional[str] = ...,
    ) -> Try_[T]: ...
    def recover(self, f: Callable[[Exception], T]) -> Try_[T]: ...
    def recoverWith(self, f: Callable[[Exception], Try_[T]]) -> Try_[T]: ...
    def failed(self) -> Try_[Exception]: ...

class Failure(Try_[T]):
    @staticmethod
    def __len__() -> int: ...
    def __init__(self, e: Any): ...
    def __eq__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
    def get(self) -> T: ...
    def getOrElse(self, default: T) -> T: ...
    def orElse(self, default: Try_[T]) -> Try_[T]: ...
    def map(self, f: Callable[[T], U]) -> Failure[U]: ...
    def flatMap(self, f: Callable[[T], Try_[U]]) -> Failure[U]: ...
    def filter(
        self,
        f: Callable[[T], bool],
        exception_cls: Type[Exception] = ...,
        msg: Optional[str] = ...,
    ) -> Failure[T]: ...
    def recover(self, f: Callable[[Exception], U]) -> Try_[U]: ...
    def recoverWith(self, f: Callable[[Exception], Try_[U]]) -> Try_[U]: ...
    def failed(self) -> Try_[Exception]: ...

@overload
def Try(f: Callable[..., T], *args, **kwargs) -> Try_[T]: ...
@overload
def Try(f: Generator[Any, T, Any], args) -> Try_[T]: ...
@overload
def Try(f: Iterator[T]) -> Try_[T]: ...
