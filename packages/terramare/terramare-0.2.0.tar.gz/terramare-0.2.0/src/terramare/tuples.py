"""Deserializer for a (typed) tuple."""

import itertools
from typing import Sequence, Tuple, cast

import attr

from . import factories, iterator_utils, type_utils
from .errors import InternalDeserializationError, InternalDeserializerFactoryError
from .types import DeserializableType, Deserializer, Primitive, T


class TupleDeserializationError(InternalDeserializationError):
    """Raised when a primitive cannot be deserialized as a tuple."""


@attr.s(auto_attribs=True, frozen=True)
class TupleDeserializer(Deserializer[T]):
    """Deserializer for a (typed) tuple."""

    _tuple_t: DeserializableType
    _untyped_list_deserializer: Deserializer[list]
    _tuple_param_deserializers: Sequence[Deserializer]

    def __call__(self, value: Primitive) -> T:
        """Deserialize a primitive as a tuple of several types."""
        try:
            value_list = self._untyped_list_deserializer(value)
        except InternalDeserializationError:
            raise TupleDeserializationError(
                value, self._tuple_t, "not a list"
            ) from None

        try:
            zipped = iterator_utils.zip_strict(
                self._tuple_param_deserializers, [], value_list
            )
        except ValueError as e:
            raise TupleDeserializationError(
                value, self._tuple_t, cause=e,
            )

        results, errors = iterator_utils.accumulate_errors_l(
            InternalDeserializationError, iter(zipped)
        )
        if errors:
            raise TupleDeserializationError(
                value, self._tuple_t, cause={f"at index {i}": e for i, e in errors},
            )

        return cast(T, tuple(v for _, v in results))


class TupleDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a tuple deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class TupleDeserializerFactory(factories.DeserializerFactory):
    """Create deserializer for a tuple type."""

    def create_deserializer_recursive(
        self, recurse_factory: factories.DeserializerFactory, type_: DeserializableType
    ) -> Deserializer[T]:
        """Create a deserializer for the specified tuple type."""
        if not type_utils.get_base_of_generic_type(type_) == Tuple:
            raise TupleDeserializerFactoryError(type_, "not a tuple type")

        deserializers, errors = iterator_utils.accumulate_errors_l(
            InternalDeserializerFactoryError,
            zip(
                itertools.repeat(recurse_factory.create_deserializer_internal),
                type_utils.get_type_parameters(type_),
            ),
        )
        if errors:
            raise TupleDeserializerFactoryError(
                type_,
                TupleDeserializerFactoryError.cannot_create_msg("tuple"),
                {f"at index {i}": e for i, e in errors},
            )

        return TupleDeserializer(
            type_,
            recurse_factory.create_deserializer_internal(list),
            [ds for _, ds in deserializers],
        )
