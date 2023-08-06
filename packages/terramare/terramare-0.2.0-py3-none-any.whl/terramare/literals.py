"""Deserializer for a literal."""

from typing import Any, Mapping

import attr
from typing_extensions import Literal

from . import factories, iterator_utils, type_utils
from .errors import InternalDeserializationError, InternalDeserializerFactoryError
from .types import DeserializableType, Deserializer, Primitive, T


class LiteralDeserializationError(InternalDeserializationError):
    """Raised when a primitive cannot be deserialized as a literal."""


@attr.s(auto_attribs=True, frozen=True)
class _SingleLiteralDeserializer(Deserializer[T]):
    deserializer: Deserializer
    value: Any

    def __call__(self, value: Primitive) -> T:
        v = self.deserializer(value)
        if v == self.value:
            return v
        raise LiteralDeserializationError(
            value,
            Literal[self.value],
            "value mismatch - expected '{}', got '{}'".format(self.value, v),
        )


# TODO reduce duplication w/ enums, unions modules
@attr.s(auto_attribs=True, frozen=True)
class LiteralDeserializer(Deserializer[T]):
    """Deserializer for a literal type."""

    _literal_t: DeserializableType
    _literal_deserializers: Mapping[str, _SingleLiteralDeserializer]

    def __call__(self, value: Primitive) -> T:
        """Deserialize a primitive as a literal type."""
        errors_ = {}
        for desc, ds in self._literal_deserializers.items():
            try:
                return ds(value)
            except InternalDeserializationError as e:
                errors_[f"variant {desc}"] = e
        raise LiteralDeserializationError(
            value,
            self._literal_t,
            cause=(errors_ if len(errors_) > 1 else list(errors_.values())[0]),
            always_display_msg=True,
        )


class LiteralDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a literal deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class LiteralDeserializerFactory(factories.DeserializerFactory):
    """Create deserializer for a literal type."""

    def create_deserializer_recursive(
        self, recurse_factory: factories.DeserializerFactory, type_: DeserializableType
    ) -> Deserializer[T]:
        """Create a deserializer for the specified literal type."""
        if not type_utils.get_base_of_generic_type(type_) == Literal:
            raise LiteralDeserializerFactoryError(type_, "not a literal type")

        deserializers, errors = iterator_utils.accumulate_errors_d(  # type: ignore[var-annotated]
            InternalDeserializerFactoryError,
            {
                str(type_param): (
                    lambda l: _SingleLiteralDeserializer(
                        deserializer=recurse_factory.create_deserializer_internal(
                            _get_literal_t(l)
                        ),
                        value=l,
                    ),
                    type_param,
                )
                for type_param in type_utils.get_type_parameters(type_)
            },
        )
        if errors:
            raise LiteralDeserializerFactoryError(
                type_,
                LiteralDeserializerFactoryError.cannot_create_msg("literal"),
                {f"variant {k}": e for k, e in errors.items()},
            )
        return LiteralDeserializer(type_, deserializers)


def _get_literal_t(type_: type) -> type:
    if type_utils.get_base_of_generic_type(type_) == Literal:
        return type_
    return type(type_)
