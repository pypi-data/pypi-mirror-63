"""Deserializer for a generic class."""

import functools
from typing import Callable, Mapping, Optional, Sequence

import attr

from . import iterator_utils
from .errors import InternalDeserializationError
from .types import Deserializer, Primitive, T


class ClassDeserializationError(InternalDeserializationError):
    """Raised when a primitive cannot be deserialized into a class."""


@attr.s(auto_attribs=True, frozen=True)
class ClassValueDeserializer(Deserializer[T]):
    """Deserialize a class from a single value."""

    _fn: Callable[..., T]
    _value_deserializer: Deserializer

    def __call__(self, value: Primitive) -> T:
        """Deserialize a primitive into parameters for a function call."""
        try:
            arg = self._value_deserializer(value)
        except InternalDeserializationError as e:
            raise ClassDeserializationError(value, self._fn, cause=e) from None
        return self._fn(arg)


@attr.s(auto_attribs=True, frozen=True)
class ClassListDeserializer(Deserializer[T]):
    """Deserialize a class from a list."""

    _fn: Callable[..., T]
    _list_deserializer: Deserializer[list]
    _required_param_deserializers: Sequence[Deserializer]
    _optional_param_deserializers: Sequence[Deserializer]
    _var_positional_deserializer: Optional[Deserializer]

    def __call__(self, value: Primitive) -> T:
        """Deserialize a primitive into parameters for a function call."""
        try:
            arg_list = self._list_deserializer(value)
        except InternalDeserializationError:
            raise ClassDeserializationError(value, self._fn, "not a list") from None

        try:
            zipped = (
                functools.partial(  # type: ignore[operator]
                    iterator_utils.zip_strict_extra, self._var_positional_deserializer
                )
                if self._var_positional_deserializer
                else iterator_utils.zip_strict
            )(
                self._required_param_deserializers,
                self._optional_param_deserializers,
                arg_list,
            )
        except ValueError as e:
            raise ClassDeserializationError(value, self._fn, cause=e) from None

        results, errors = iterator_utils.accumulate_errors_l(
            InternalDeserializationError, iter(zipped)
        )

        if errors:
            raise ClassDeserializationError(
                value, self._fn, cause={f"at index {i}": e for i, e in errors},
            )
        return self._fn(*[v for _, v in results])


@attr.s(auto_attribs=True, frozen=True)
class ClassDictDeserializer(Deserializer[T]):
    """Deserialize a class from a dictionary."""

    _fn: Callable[..., T]
    _dict_deserializer: Deserializer[dict]
    _required_param_deserializers: Mapping[str, Deserializer]
    _optional_param_deserializers: Mapping[str, Deserializer]
    _var_keyword_deserializer: Optional[Deserializer]

    def __call__(self, value: Primitive) -> T:
        """Deserialize a primitive into parameters for a function call."""
        try:
            arg_dict = self._dict_deserializer(value)
        except InternalDeserializationError:
            raise ClassDeserializationError(value, self._fn, "not a dict") from None

        try:
            zipped = (
                functools.partial(  # type: ignore[operator]
                    iterator_utils.zip_strict_dict_extra, self._var_keyword_deserializer
                )
                if self._var_keyword_deserializer
                else iterator_utils.zip_strict_dict
            )(
                self._required_param_deserializers,
                self._optional_param_deserializers,
                arg_dict,
            )
        except ValueError as e:
            raise ClassDeserializationError(
                value, self._fn, cause=e,
            )

        results, errors = iterator_utils.accumulate_errors_d(
            InternalDeserializationError, zipped
        )

        if errors:
            raise ClassDeserializationError(
                value, self._fn, cause={f'at key "{k}"': e for k, e in errors.items()},
            )
        return self._fn(**results)


@attr.s(auto_attribs=True, frozen=True)
class ClassDeserializer(Deserializer[T]):
    """Deserialize a class."""

    _fn: Callable[..., T]
    _deserializers: Mapping[str, Deserializer[T]]

    def __call__(self, value: Primitive) -> T:
        """Deserialize a primitive as a class."""
        errors_ = {}
        for desc, ds in self._deserializers.items():
            try:
                return ds(value)
            except InternalDeserializationError as e:
                errors_[desc] = e
        raise ClassDeserializationError(
            value, self._fn, cause=errors_, always_display_msg=True
        )
