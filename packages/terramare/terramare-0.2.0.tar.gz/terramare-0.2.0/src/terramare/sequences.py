"""Deserializer for a generalized homogenous sequence."""

import itertools
from typing import (
    Callable,
    FrozenSet,
    Generic,
    Iterable,
    Iterator,
    List,
    MutableSequence,
    Sequence,
    Set,
    TypeVar,
)

import attr

from . import factories, iterator_utils, pretty_printer, type_utils
from .errors import InternalDeserializationError, InternalDeserializerFactoryError
from .types import DeserializableType, Deserializer, Primitive, T


class SequenceDeserializationError(InternalDeserializationError):
    """Raised when failing to deserialize a (typed) generalized sequence."""


S = TypeVar("S")


@attr.s(auto_attribs=True, frozen=True)
class SequenceDeserializer(Generic[S, T], Deserializer[T]):
    """Deserializer for a sequence of values of the same type."""

    _sequence_t: DeserializableType
    _untyped_list_deserializer: Deserializer[list]
    _element_deserializer: Deserializer[S]
    _constructor_fn: Callable[[Iterator[S]], T]

    def __call__(self, value: Primitive) -> T:
        """Deserialize a primitive as a (typed) sequence."""
        try:
            value_list = self._untyped_list_deserializer(value)
        except InternalDeserializationError as e:
            raise SequenceDeserializationError(
                value, self._sequence_t, cause=e, always_display_msg=True
            )

        results, errors = iterator_utils.accumulate_errors_l(
            InternalDeserializationError,
            zip(itertools.repeat(self._element_deserializer), value_list),
        )
        if errors:
            raise SequenceDeserializationError(
                value, self._sequence_t, cause={f"at index {i}": e for i, e in errors},
            )
        return self._constructor_fn(v for _, v in results)


class SequenceDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a (typed) generalized sequence deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class SequenceDeserializerFactory(factories.DeserializerFactory):
    """Create deserializer for a generalized homogenous sequence type."""

    def create_deserializer_recursive(
        self, recurse_factory: factories.DeserializerFactory, type_: DeserializableType
    ) -> Deserializer[T]:
        """Create a deserializer for the specified homogeneous sequence type."""
        sequence_constructors = {
            FrozenSet: set,
            Iterable: list,
            Iterator: iter,
            List: list,
            MutableSequence: list,
            Sequence: list,
            Set: set,
        }
        base = type_utils.get_base_of_generic_type(type_)
        if base not in sequence_constructors:
            raise SequenceDeserializerFactoryError(type_, "not a sequence type")

        [value_type] = type_utils.get_type_parameters(type_)
        try:
            deserializer = recurse_factory.create_deserializer_internal(value_type)
        except InternalDeserializerFactoryError as e:
            raise SequenceDeserializerFactoryError(
                type_,
                SequenceDeserializerFactoryError.cannot_create_msg(
                    pretty_printer.print_type_name(base)
                ),
                e,
            ) from None

        return SequenceDeserializer(
            type_,
            recurse_factory.create_deserializer_internal(list),
            deserializer,
            sequence_constructors[base],  # type: ignore[arg-type, index]
        )
