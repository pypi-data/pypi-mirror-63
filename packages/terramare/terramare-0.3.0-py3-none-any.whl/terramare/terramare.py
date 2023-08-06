"""Automatically deserialize complex objects from simple Python types."""

from typing import Callable, FrozenSet, Type

from . import (
    classes,
    dicts,
    enums,
    errors,
    factories,
    literals,
    newtypes,
    primitives,
    sequences,
    tuples,
    unions,
)
from .types import DeserializableType, Primitive, T

DEFAULT_TRUE_STRINGS = frozenset({"yes", "on", "true", "1"})
DEFAULT_FALSE_STRINGS = frozenset({"no", "off", "false", "0"})
DEFAULT_EXCEPTION_TYPES_TO_HANDLE: FrozenSet[Type[Exception]] = frozenset()


def deserialize_into(
    type_: DeserializableType,
    value: Primitive,
    coerce_strings: bool = False,
    true_strings: FrozenSet[str] = DEFAULT_TRUE_STRINGS,
    false_strings: FrozenSet[str] = DEFAULT_FALSE_STRINGS,
    handle_exception_types: FrozenSet[
        Type[Exception]
    ] = DEFAULT_EXCEPTION_TYPES_TO_HANDLE,
    handle_reentrancy: bool = False,
) -> T:
    """
    Deserialize a primitive as a value of the specified type.

    :param `type_`: Deserialize into this type.
    :param `value`: Primitive value to attempt to deserialize.
    :param `coerce_strings`: If set, attempt to convert :python:`str` values to
        :python:`bool`, :python:`int`, or :python:`float` where the latter are required.
        For example:

        >>> deserialize_into(int, "1")
        Traceback (most recent call last):
            ...
        terramare.errors.DeserializationError: ...
        >>> deserialize_into(int, "1", coerce_strings=True)
        1

        This option defaults to :python:`False`.

    :param `true_strings`: Set of strings to convert to :python:`True` when convering a
        :python:`str` value to a :python:`bool`. Case is ignored.

        This value defaults to :python:`{"yes", "on", "true", "1"}`.

    :param `false_strings`: Set of strings to convert to :python:`False` when convering
        a :python:`str` value to a :python:`bool`. Case is ignored.

        This value defaults to :python:`{"no", "off", "false", "0"}`.

    :param `handle_exception_types`: Set of additional exception types that
        :python:`terramare` should catch and handle rather than propogating.

        Generally this will still result in an exception being raised. However, it will
        be a :python:`terramare` exception containing additional context.

        This option is useful when the deserialization target provides some form of
        additional validation. For example:

        >>> from typing import Union
        >>> import attr
        >>>
        >>> @attr.s
        ... class Paint:
        ...    color: str = attr.ib(validator=attr.validators.in_(["red", "blue"]))

        When no exception types are provided, context is lost when deserializing into a
        single type:

        >>> deserialize_into(Paint, "green")
        Traceback (most recent call last):
        ...
        ValueError: 'color' must be in ['red', 'blue'] (got 'green')

        When the exception type is provided, that context is preserved:

        >>> deserialize_into(Paint, "green", handle_exception_types={ValueError})
        Traceback (most recent call last):
        ...
        terramare.errors.DeserializationError: cannot read value '"green"' into 'Paint': 'color' must be in ['red', 'blue'] (got 'green')

        The exception is when the deserialization target is a union type, where
        :python:`terramare` will continue to try further union variants - as it would
        when encountering a deserialization failure.

        When no exception types are provided, :python:`terramare` cannot try further
        union variants if one fails due to a validation error:

        >>> deserialize_into(Union[Paint, str], "green")
        Traceback (most recent call last):
        ...
        ValueError: 'color' must be in ['red', 'blue'] (got 'green')

        When the exception type is provided, :python:`terramare` continues and
        successfully deserializes into a later variant.

        >>> deserialize_into(Union[Paint, str], "green", handle_exception_types={ValueError})
        'green'

    :param `handle_reentrancy`: This option determines :python:`terramare`'s behaviour
        when deserializing into a class or function that itself invokes
        :python:`terramare`:

        - If set to :python:`True`, :python:`terramare` will catch and handle exceptions
          raised by calls back into :python:`terramare`. This setting is useful when
          deserializing in several stages, common when the type of some later member
          depends on the value of an earlier one.

        - If set to :python:`False`, :python:`terramare` will not catch these exceptions,
          propogating them as normal. This is a safer setting when the expectation is
          that deserializion will not have multiple stages, that is, when
          :python:`terramare` exceptions raised by re-entrancy are unexpected and should
          be propogated.

        For example:

        >>> from typing import Any, List, Union
        >>> import attr
        >>>
        >>> @attr.s(auto_attribs=True)
        ... class PythonConfig:
        ...    pip_path: str
        >>>
        >>> @attr.s(auto_attribs=True)
        ... class BashConfig:
        ...     set_options: List[str]
        >>>
        >>> def load_language_config(
        ...     language: str,
        ...     **remainder: Any
        ... ) -> "Union[PythonConfig, BashConfig]":
        ...     if language == "python":
        ...         return deserialize_into(PythonConfig, remainder)
        ...     elif language == "bash":
        ...         return deserialize_into(PythonConfig, remainder)
        ...     else:
        ...         raise NotImplementedError
        >>>
        >>> data = {"language": "python", "set_options": "xe"}

        When handling re-entrancy is disabled, the :python:`load_language_context` is
        lost:

        >>> deserialize_into(load_language_config, data)
        Traceback (most recent call last):
        ...
        terramare.errors.DeserializationError: cannot read value ... into 'PythonConfig':
        ...

        When handling re-entrancy is enabled, that context is preserved:

        >>> deserialize_into(load_language_config, data, handle_reentrancy=True)
        Traceback (most recent call last):
        ...
        terramare.errors.DeserializationError: cannot read value ... into 'load_language_config':
        ...

    :raises terramare.DeserializerFactoryError: if a deserializer for :python:`type_`
        cannot be created.
    :raises terramare.DeserializationError: if the deserializer fails to deserialize a
        value of :python:`type_` from :python:`value`.
    """  # noqa: F401, E501
    return create_deserializer_factory(
        coerce_strings=coerce_strings,
        true_strings=true_strings,
        false_strings=false_strings,
        handle_exception_types=handle_exception_types,
        handle_reentrancy=handle_reentrancy,
    ).deserialize_into(type_, value)


def create_deserializer_factory(
    coerce_strings: bool = False,
    true_strings: FrozenSet[str] = DEFAULT_TRUE_STRINGS,
    false_strings: FrozenSet[str] = DEFAULT_FALSE_STRINGS,
    handle_exception_types: FrozenSet[
        Type[Exception]
    ] = DEFAULT_EXCEPTION_TYPES_TO_HANDLE,
    handle_reentrancy: bool = False,
) -> factories.DeserializerFactory:
    """Create a DeserializerFactory using sensible defaults which may be overridden."""

    def class_deserializer_enable_if(t: DeserializableType) -> bool:
        return getattr(t, "__origin__", None) is not Callable

    return factories.CachingDeserializerFactory.new(
        factories.SequenceDeserializerFactory(
            {
                "newtype": newtypes.NewTypeDeserializerFactory(),
                "primitive": primitives.PrimitiveDeserializerFactory(
                    coerce_strings=coerce_strings,
                    true_strings=frozenset(s.lower() for s in true_strings),
                    false_strings=frozenset(s.lower() for s in false_strings),
                ),
                "literal": literals.LiteralDeserializerFactory(),
                "tuple": tuples.TupleDeserializerFactory(),
                "union": unions.UnionDeserializerFactory(),
                "sequences": sequences.HomogeneousSequenceDeserializerFactory(),
                "dict": dicts.DictDeserializerFactory(),
                "enum": enums.EnumDeserializerFactory(),
                "class": classes.ClassDeserializerFactory(
                    enable_if=class_deserializer_enable_if,
                    handle_exception_ts=handle_exception_types
                    | frozenset(
                        {errors.DeserializationError} if handle_reentrancy else {}
                    ),
                ),
            }
        )
    )
