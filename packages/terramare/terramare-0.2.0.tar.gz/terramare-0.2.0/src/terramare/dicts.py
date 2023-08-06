"""Deserializer for a dictionary."""

import itertools
from typing import Dict, List, Mapping, MutableMapping, Set

import attr

from . import factories, iterator_utils, pretty_printer, type_utils
from .errors import InternalDeserializationError, InternalDeserializerFactoryError
from .types import DeserializableType, Deserializer, Primitive, T


class DictDeserializationError(InternalDeserializationError):
    """Raised when a primitive cannot be deserialized as a dict."""


@attr.s(auto_attribs=True, frozen=True)
class DictDeserializer(Deserializer[Dict[str, T]]):
    """Deserializer for a (homogeneous) dictionary."""

    _dict_t: DeserializableType
    _untyped_dict_deserializer: Deserializer[dict]
    _key_deserializer: Deserializer[str]
    _value_deserializer: Deserializer[T]

    def __call__(self, value: Primitive) -> Dict[str, T]:
        """Deserialize a primitive as a (homogeneous) dictionary."""
        try:
            value_dict = self._untyped_dict_deserializer(value)
        except InternalDeserializationError as e:
            raise DictDeserializationError(
                value, self._dict_t, cause=e, always_display_msg=True
            ) from None

        keys, key_errors = iterator_utils.accumulate_errors_l(
            InternalDeserializationError,
            zip(itertools.repeat(self._key_deserializer), value_dict.keys()),
        )

        results, value_errors = iterator_utils.accumulate_errors_d(
            InternalDeserializationError,
            {k: (self._value_deserializer, value_dict[k]) for _, k in keys},
        )

        if key_errors or value_errors:
            raise DictDeserializationError(
                value,
                self._dict_t,
                cause={
                    **{f"at index {i}": e for i, e in key_errors},
                    **{f'at key "{k}': e for k, e in value_errors.items()},
                },
            )
        return results


class DictDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a dict deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class DictDeserializerFactory(factories.DeserializerFactory):
    """Create deserializer for a dictionary of values of the same type."""

    def create_deserializer_recursive(
        self, recurse_factory: factories.DeserializerFactory, type_: DeserializableType
    ) -> Deserializer[T]:
        """Create a deserializer for the specified dictionary type."""
        if type_utils.get_base_of_generic_type(type_) not in {
            Dict,
            Mapping,
            MutableMapping,
        }:
            raise DictDeserializerFactoryError(type_, "not a dict type")

        key_type, value_type = type_utils.get_type_parameters(type_)
        if not _is_hashable(key_type):
            raise DictDeserializerFactoryError(
                type_,
                "unhashable key type: '{}'".format(
                    pretty_printer.print_type_name(key_type)
                ),
            )

        deserializers, errors = iterator_utils.accumulate_errors_d(
            InternalDeserializerFactoryError,
            {
                "key": (recurse_factory.create_deserializer_internal, key_type),
                "value": (recurse_factory.create_deserializer_internal, value_type),
            },
        )
        if errors:
            raise DictDeserializerFactoryError(
                type_,
                DictDeserializerFactoryError.cannot_create_msg("dict"),
                {f"{k} type": e for k, e in errors.items()},
            )
        return DictDeserializer(  # type: ignore[return-value]
            type_,
            recurse_factory.create_deserializer_internal(dict),
            deserializers["key"],
            deserializers["value"],
        )


def _is_hashable(type_: DeserializableType) -> bool:
    return (
        "__hash__" in dir(type_)
        and "__eq__" in dir(type_)
        and type_utils.get_base_of_generic_type(type_) not in {Dict, List, Set}
    )
