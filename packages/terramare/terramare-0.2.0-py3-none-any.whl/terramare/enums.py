"""Deserializer for an enum."""

import enum
from typing import Any, Dict, Mapping

import attr

from . import factories, iterator_utils
from .errors import InternalDeserializationError, InternalDeserializerFactoryError
from .types import DeserializableType, Deserializer, Primitive, T


class EnumDeserializationError(InternalDeserializationError):
    """Raised when a primitive cannot be deserialized as any value of an enum."""


@attr.s(auto_attribs=True, frozen=True)
class _SingleEnumValueDeserializer(Deserializer[T]):
    enum_t: DeserializableType
    deserializer: Deserializer
    variant: Any

    def __call__(self, value: Primitive) -> T:
        v = self.deserializer(value)
        if v == self.variant.value:
            return self.variant
        raise EnumDeserializationError(
            v,
            self.variant,
            msg=f"value mismatch {repr(v)} - expected {repr(self.variant.value)}",
            always_display_msg=True,
        )


@attr.s(auto_attribs=True, frozen=True)
class EnumDeserializer(Deserializer[T]):
    """Deserializer for an enum type."""

    _enum_t: DeserializableType
    _enum_value_deserializers: Mapping[str, _SingleEnumValueDeserializer]

    def __call__(self, value: Primitive) -> T:
        """Deserialize a primitive as an enum value."""
        errors_: Dict[str, Exception] = {}
        for desc, ds in self._enum_value_deserializers.items():
            try:
                return ds(value)
            except InternalDeserializationError as e:
                errors_[desc] = e
        raise EnumDeserializationError(
            value, self._enum_t, cause=errors_,
        )


class EnumDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create an enum deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class EnumDeserializerFactory(factories.DeserializerFactory):
    """Create deserializer for an enum type."""

    def create_deserializer_recursive(
        self, recurse_factory: factories.DeserializerFactory, type_: DeserializableType
    ) -> Deserializer[T]:
        """Create deserializer for the specified enum type."""
        if not (isinstance(type_, type) and issubclass(type_, enum.Enum)):
            raise EnumDeserializerFactoryError(type_, "not an enum type")

        deserializers, errors = iterator_utils.accumulate_errors_d(  # type: ignore[var-annotated]
            InternalDeserializerFactoryError,
            {  # type: ignore[var-annotated]
                f"variant <{variant.name}: {repr(variant.value)}>": (
                    lambda v: _SingleEnumValueDeserializer(
                        enum_t=type_,
                        deserializer=recurse_factory.create_deserializer_internal(
                            type(v.value)
                        ),
                        variant=v,
                    ),
                    variant,
                )
                for variant in list(type_)
            },
        )
        if errors:
            raise EnumDeserializerFactoryError(
                type_,
                EnumDeserializerFactoryError.cannot_create_msg("enum"),
                {k: e for k, e in errors.items()},
            )
        return EnumDeserializer(type_, deserializers)
