"""Automatically deserialize complex objects from simple Python types."""

from typing import Any, Callable, FrozenSet, Optional

from . import (
    classes_factory,
    dicts,
    enums,
    factories,
    literals,
    newtypes,
    primitives,
    sequences,
    tuples,
    unions,
)
from .types import DeserializableType, Deserializer, Primitive, T

DEFAULT_TRUE_STRINGS = frozenset({"yes", "on", "true", "1"})
DEFAULT_FALSE_STRINGS = frozenset({"no", "off", "false", "0"})


def create_deserializer(
    type_: DeserializableType, **kwargs: Any,
) -> Deserializer[T]:  # pragma: no cover
    """
    Create a deserializer for the specified type.

    :param `type_`: Deserialize into this type.
    :param `**kwargs`: Passed unmodified to `create_deserializer_factory`.
    :raises terramare.DeserializerFactoryError: if the deserializer cannot be created.
    """
    return create_deserializer_factory(**kwargs).create_deserializer(type_)


def deserialize_into(type_: DeserializableType, value: Primitive, **kwargs: Any) -> T:
    """
    Deserialize a primitive as a value of the specified type.

    :param `type_`: Deserialize into this type.
    :param `value`: Primitive value to attempt to deserialize.
    :param `**kwargs`: Passed unmodified to `create_deserializer_factory`.
    :raises terramare.DeserializerFactoryError: if a deserializer for `type_`
        cannot be created.
    :raises terramare.DeserializationError: if the deserializer fails to deserialize a
        value of `type_` from `value`.
    """
    return create_deserializer_factory(**kwargs).deserialize_into(type_, value)


def create_deserializer_factory(
    coerce_strings: bool = False,
    true_strings: Optional[FrozenSet[str]] = None,
    false_strings: Optional[FrozenSet[str]] = None,
) -> factories.DeserializerFactory:
    """
    Create a DeserializerFactory using sensible defaults which may be overridden.

    :param `coerce_strings`: If set, attempt to convert `str` values to `bool`, `int`,
        or `float` where the latter are required. For example:

        >>> deserialize_into(int, "1")
        Traceback (most recent call last):
            ...
        terramare.primitives.PrimitiveDeserializationError: ...
        >>> deserialize_into(int, "1", coerce_strings=True)
        1

    :param `true_strings`: Set of strings to convert to `True` when convering a `str`
        value to a `bool`. Case is ignored. Defaults to `{"yes", "on", "true", "1"}`.
    :param `false_strings`: Set of strings to convert to `False` when convering a `str`
        value to a `bool`. Case is ignored. Defaults to `{"no", "off", "false", "0"}`.
    """
    if true_strings is None:  # pragma: no branch
        true_strings = DEFAULT_TRUE_STRINGS
    if false_strings is None:  # pragma: no branch
        false_strings = DEFAULT_FALSE_STRINGS

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
                "sequences": sequences.SequenceDeserializerFactory(),
                "dict": dicts.DictDeserializerFactory(),
                "enum": enums.EnumDeserializerFactory(),
                "class": classes_factory.ClassDeserializerFactory(
                    enable_if=class_deserializer_enable_if
                ),
            }
        )
    )
