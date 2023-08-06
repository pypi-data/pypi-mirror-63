"""Deserializer factory for a generic class."""

import inspect
import sys
import typing
from inspect import Parameter
from typing import Any, Callable, Dict, List, Sequence, TypeVar

import attr

from . import classes, factories, iterator_utils
from .errors import InternalDeserializerFactoryError
from .types import DeserializableType, Deserializer, T

S = TypeVar("S")


def _is_var(parameter: inspect.Parameter) -> bool:
    return parameter.kind in {Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD}


def _is_pos(parameter: inspect.Parameter) -> bool:
    return parameter.kind in {
        Parameter.POSITIONAL_ONLY,
        Parameter.POSITIONAL_OR_KEYWORD,
        Parameter.VAR_POSITIONAL,
    }


def _is_kw(parameter: inspect.Parameter) -> bool:
    return parameter.kind in {
        Parameter.KEYWORD_ONLY,
        Parameter.POSITIONAL_OR_KEYWORD,
        Parameter.VAR_KEYWORD,
    }


def _is_required(parameter: inspect.Parameter) -> bool:
    return parameter.default == inspect.Parameter.empty and not _is_var(parameter)


class ClassDeserializerFactoryError(InternalDeserializerFactoryError):
    """Raised when failing to create a class deserializer."""


@attr.s(auto_attribs=True, frozen=True)
class ClassDeserializerFactory(factories.DeserializerFactory):
    """Create deserializer for a class."""

    enable_if: Callable[[DeserializableType], bool] = lambda _: True

    def create_deserializer_recursive(
        self, recurse_factory: factories.DeserializerFactory, type_: DeserializableType
    ) -> Deserializer[T]:
        """Create a deserializer for the specified class type."""
        if not self.enable_if(type_):
            raise ClassDeserializerFactoryError(type_, "disabled for type")
        if not hasattr(type_, "__call__"):
            raise ClassDeserializerFactoryError(type_, "not a callable type")

        parameters = _get_parameters(type_)
        class_deserializers = {}
        errors = {}
        for desc, fn in {
            "from dict": _create_class_dict_deserializer,
            "from list": _create_class_list_deserializer,
            "from value": _create_class_value_deserializer,
        }.items():
            try:
                class_deserializers[desc] = fn(recurse_factory, type_, parameters)
            except InternalDeserializerFactoryError as e:
                errors[desc] = e
        if class_deserializers:
            return classes.ClassDeserializer(type_, class_deserializers)
        raise ClassDeserializerFactoryError(
            type_, ClassDeserializerFactoryError.cannot_create_msg("class"), errors
        )


def _create_class_value_deserializer(
    recurse_factory: factories.DeserializerFactory,
    type_: DeserializableType,
    parameters: Sequence[inspect.Parameter],
) -> classes.ClassValueDeserializer:
    required, optional = iterator_utils.divide_list(_is_required, parameters)
    if len(required) > 1 or len(required) + len(optional) < 1:
        raise ClassDeserializerFactoryError(
            type_,
            "unsupported number of parameters "
            "(required: {}, optional: {})".format(len(required), len(optional)),
        )

    value_parameter = parameters[0]
    if not _is_pos(value_parameter):
        raise ClassDeserializerFactoryError(
            type_, "non-positional first parameter {}".format(value_parameter.name),
        )
    return classes.ClassValueDeserializer(
        type_,
        _get_deserializers(recurse_factory, type_, [value_parameter])[
            value_parameter.name
        ],
    )


def _create_class_list_deserializer(
    recurse_factory: factories.DeserializerFactory,
    type_: DeserializableType,
    parameters: Sequence[inspect.Parameter],
) -> classes.ClassListDeserializer:
    non_pos_required = [
        p.name for p in parameters if _is_required(p) and not _is_pos(p)
    ]
    if non_pos_required:
        raise ClassDeserializerFactoryError(
            type_,
            "required non-positional parameter(s) {}".format(
                ", ".join(non_pos_required)
            ),
        )

    pos = [p for p in parameters if _is_pos(p)]
    deserializers = _get_deserializers(recurse_factory, type_, pos)
    var_pos, non_var_pos = iterator_utils.divide_list(_is_var, pos)
    return classes.ClassListDeserializer(
        type_,
        recurse_factory.create_deserializer_internal(list),
        [deserializers[p.name] for p in non_var_pos if _is_required(p)],
        [deserializers[p.name] for p in non_var_pos if not _is_required(p)],
        iterator_utils.get_single_element([deserializers[p.name] for p in var_pos]),
    )


def _create_class_dict_deserializer(
    recurse_factory: factories.DeserializerFactory,
    type_: DeserializableType,
    parameters: Sequence[inspect.Parameter],
) -> classes.ClassDictDeserializer:
    non_kw_required = [p.name for p in parameters if _is_required(p) and not _is_kw(p)]
    if non_kw_required:  # pragma: no cover TODO
        raise ClassDeserializerFactoryError(
            type_,
            "required non-keyword parameter(s) {}".format(", ".join(non_kw_required)),
        )

    kw = [p for p in parameters if _is_kw(p)]
    deserializers = _get_deserializers(recurse_factory, type_, kw)
    var_kw, non_var_kw = iterator_utils.divide_list(_is_var, kw)
    return classes.ClassDictDeserializer(
        type_,
        recurse_factory.create_deserializer_internal(dict),
        {p.name: deserializers[p.name] for p in non_var_kw if _is_required(p)},
        {p.name: deserializers[p.name] for p in non_var_kw if not _is_required(p)},
        iterator_utils.get_single_element([deserializers[p.name] for p in var_kw]),
    )


def _get_parameters(type_: DeserializableType) -> List[inspect.Parameter]:
    try:
        return list(inspect.signature(type_).parameters.values())
    except ValueError as e:
        raise ClassDeserializerFactoryError(
            type_,
            ClassDeserializerFactoryError.cannot_create_msg("class"),
            e,
            always_display_msg=True,
        )


def _get_deserializers(
    recurse_factory: factories.DeserializerFactory,
    type_: DeserializableType,
    parameters: List[inspect.Parameter],
) -> Dict[str, Deserializer]:
    type_hints = _get_type_hints(type_, parameters)
    deserializers, errors = iterator_utils.accumulate_errors_d(
        InternalDeserializerFactoryError,
        {
            parameter.name: (
                lambda p: recurse_factory.create_deserializer_internal(
                    type_hints[p.name]
                ),
                parameter,
            )
            for parameter in parameters
        },
    )

    if errors:
        raise ClassDeserializerFactoryError(
            type_,
            ClassDeserializerFactoryError.cannot_create_msg("class"),
            {f'parameter "{k}"': e for k, e in errors.items()},
        )
    return deserializers


def _get_type_hints(
    type_: DeserializableType, params: Sequence[Parameter]
) -> Dict[str, Any]:
    if hasattr(type_, "__globals__"):
        globals_ = getattr(type_, "__globals__")
    elif hasattr(type_, "__module__"):
        globals_ = vars(sys.modules[getattr(type_, "__module__")])
    else:  # pragma: no cover TODO
        globals_ = {}

    try:
        type_hints = typing.get_type_hints(type_, globals_)
    except TypeError as e:  # pragma: no cover
        raise ClassDeserializerFactoryError(
            type_, ClassDeserializerFactoryError.cannot_create_msg("class"), e
        )

    def get_type_hint(p: inspect.Parameter) -> Any:
        if p.name in type_hints:
            return type_hints[p.name]
        if p.annotation == inspect.Parameter.empty:
            return Any
        if not isinstance(p.annotation, str):
            return p.annotation
        # TODO __closure__?
        return eval(  # pragma: no cover, pylint: disable=eval-used
            p.annotation, globals_
        )

    return {p.name: get_type_hint(p) for p in params}
