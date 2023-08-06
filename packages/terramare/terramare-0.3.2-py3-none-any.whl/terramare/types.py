"""Common types."""

import abc
from typing import Any, Callable, Generic, Type, TypeVar, Union

T = TypeVar("T")


NotNonePrimitive = Union[str, int, float, dict, list, bool]
Primitive = Union[NotNonePrimitive, None]

DeserializableType = Union[Type[Any], Callable[..., Any]]


class Deserializer(abc.ABC, Generic[T]):
    """Interface implemented by deserializers."""

    @abc.abstractmethod
    def __call__(self, value: Primitive) -> T:
        """Deserialize a value."""


class TerramareError(Exception):
    """Base class for exceptions raised by terramare."""
