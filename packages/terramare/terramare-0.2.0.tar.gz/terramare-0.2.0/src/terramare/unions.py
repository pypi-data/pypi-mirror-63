"""Deserializer for a union of types."""

from typing import Mapping, Union

import attr

from . import factories, iterator_utils, pretty_printer, type_utils
from .errors import InternalDeserializationError, InternalDeserializerFactoryError
from .types import DeserializableType, Deserializer, Primitive, T


class UnionDeserializationError(InternalDeserializationError):
    """Raised when a primitive cannot be deserialized as any type in a union."""


@attr.s(auto_attribs=True, frozen=True)
class UnionDeserializer(Deserializer[T]):
    """Deserializer for a union of types."""

    _union_t: DeserializableType
    _union_param_deserializers: Mapping[str, Deserializer]

    def __call__(self, value: Primitive) -> T:
        """Deserialize a primitive as any one of a union of types."""
        errors_ = {}
        for desc, ds in self._union_param_deserializers.items():
            try:
                return ds(value)
            except InternalDeserializationError as e:
                errors_[desc] = e
        raise UnionDeserializationError(
            value, self._union_t, cause=errors_,
        )


class UnionDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a union deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class UnionDeserializerFactory(factories.DeserializerFactory):
    """Create deserializer for a union of several types."""

    def create_deserializer_recursive(
        self, recurse_factory: factories.DeserializerFactory, type_: DeserializableType
    ) -> Deserializer[T]:
        """Create a deserializer for the specified union type."""
        if not type_utils.get_base_of_generic_type(type_) == Union:
            raise UnionDeserializerFactoryError(type_, "not a union type")

        deserializers, errors = iterator_utils.accumulate_errors_d(
            InternalDeserializerFactoryError,
            {
                pretty_printer.print_type_name(type_param): (
                    recurse_factory.create_deserializer_internal,
                    type_param,
                )
                for type_param in type_utils.get_type_parameters(type_)
            },
        )
        if errors:
            raise UnionDeserializerFactoryError(
                type_,
                UnionDeserializerFactoryError.cannot_create_msg("union"),
                {t: e for t, e in errors.items()},
            )
        return UnionDeserializer(type_, deserializers)
