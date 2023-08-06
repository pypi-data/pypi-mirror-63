"""Factories used to create deserializers."""

import abc
from typing import Dict, Generic, Mapping

import attr
from typing_extensions import final

from .errors import (
    DeserializationError,
    DeserializerFactoryError,
    ErrorDisplayStrategy,
    InternalDeserializationError,
    InternalDeserializerFactoryError,
)
from .types import DeserializableType, Deserializer, Primitive, T


class DeserializerFactory(abc.ABC, Generic[T]):
    """Interface for a factory class used to create Deserializers."""

    @final
    def deserialize_into(self, type_: DeserializableType, value: Primitive) -> T:
        """Deserialize a primitive as a value of the specified type."""
        try:
            return self.create_deserializer(type_)(value)
        except InternalDeserializationError as e:  # pragma: no cover
            raise DeserializationError(**vars(e))

    @final
    def create_deserializer(self, type_: DeserializableType) -> Deserializer[T]:
        """Create a deserializer for the specified type."""
        try:
            return self.create_deserializer_internal(type_)
        except InternalDeserializerFactoryError as e:  # pragma: no cover
            raise DeserializerFactoryError(**vars(e))

    @final
    def create_deserializer_internal(
        self, type_: DeserializableType
    ) -> Deserializer[T]:
        """
        Create a deserializer, recursing with this factory.

        Used internally - does not re-raise internal exceptions.
        """
        return self.create_deserializer_recursive(self, type_)

    @abc.abstractmethod
    def create_deserializer_recursive(
        self, recurse_factory: "DeserializerFactory", type_: DeserializableType
    ) -> Deserializer[T]:
        """
        Create a deserializer, recursing with the supplied factory.

        Implemented by derived classes.
        """


@attr.s(auto_attribs=True, frozen=True)
class SequenceDeserializerFactory(DeserializerFactory):
    """Deserializer factory that tries a sequence of factories in turn."""

    _deserializer_factories: Mapping[str, DeserializerFactory]

    def create_deserializer_recursive(
        self, recurse_factory: DeserializerFactory, type_: DeserializableType
    ) -> Deserializer[T]:
        """Create a deserializer for the specified type."""
        errors_: Dict[str, InternalDeserializerFactoryError] = {}
        for desc, deserializer_factory in self._deserializer_factories.items():
            try:
                return deserializer_factory.create_deserializer_recursive(
                    recurse_factory, type_
                )
            except InternalDeserializerFactoryError as e:
                errors_[desc] = e
        raise InternalDeserializerFactoryError(
            type_,
            "cannot create deserializer for type '{}'".format(get_type_name(type_)),
            errors_,
            display_strategy=ErrorDisplayStrategy.ALWAYS_DISPLAY,
        )


def get_type_name(type_: DeserializableType) -> str:
    """Return the best available user-facing name for a type."""
    return getattr(type_, "__qualname__", str(type_))


@attr.s(auto_attribs=True, frozen=True)
class CachingDeserializerFactory(DeserializerFactory):
    """Add caching function to a DeserializerFactory."""

    _deserializer_factory: DeserializerFactory
    _cache: Dict[DeserializableType, Deserializer]

    @staticmethod
    def new(deserializer_factory: DeserializerFactory) -> "CachingDeserializerFactory":
        """Create a CachingDeserializerFactory."""
        return CachingDeserializerFactory(deserializer_factory, {})

    def create_deserializer_recursive(
        self, recurse_factory: DeserializerFactory, type_: DeserializableType
    ) -> Deserializer[T]:
        """Create a deserializer for the specified type."""
        try:
            # Don't attempt to cache non-hashable types.
            hash(type_)
        except TypeError:
            return self._deserializer_factory.create_deserializer_recursive(
                recurse_factory, type_
            )
        else:
            if type_ not in self._cache:
                self._cache[
                    type_
                ] = self._deserializer_factory.create_deserializer_recursive(
                    recurse_factory, type_
                )
            return self._cache[type_]
