"""Common error types."""

from typing import Optional, TypeVar, cast

import attr
from typing_extensions import final

from . import exception_formatter, pretty_printer
from .exception_formatter import ErrorDisplayStrategy
from .types import DeserializableType, Primitive, TerramareError

S = TypeVar("S", bound="DeserializationError")


@attr.s(auto_attribs=True, frozen=True)
class DeserializationError(TerramareError):
    """Raised when a deserializer fails."""

    value: Primitive
    target_t: DeserializableType
    cause: Optional[exception_formatter.Cause[Exception]] = None
    msg: Optional[str] = None
    display_strategy: ErrorDisplayStrategy = ErrorDisplayStrategy.DEFAULT

    @final
    def _get_msg(self) -> str:
        """Return a string description of the error."""
        if self.msg is not None:
            return self.msg
        return "cannot read value '{}' into '{}'".format(
            pretty_printer.print_primitive(self.value),
            pretty_printer.print_type_name(self.target_t),
        )

    @final
    def __str__(self) -> str:
        """Format the exception message."""

        def get_metadata(
            e: Exception,
        ) -> exception_formatter.ExceptionData[Exception, Exception]:
            if isinstance(e, DeserializationError):
                return exception_formatter.ExceptionData(
                    e,
                    e.cause if e.cause is not None else {},
                    e._get_msg(),  # pylint: disable=protected-access
                    e.display_strategy,
                )
            return exception_formatter.ExceptionData(
                e, {}, str(e), ErrorDisplayStrategy.DEFAULT
            )

        return exception_formatter.format_exception(cast(Exception, self), get_metadata)


class InternalDeserializationError(DeserializationError):
    """Raised when a deserializer fails. Caught internally."""


T = TypeVar("T", bound="DeserializerFactoryError")


@attr.s(auto_attribs=True, frozen=True)
class DeserializerFactoryError(TerramareError):
    """Raised when deserializer creation fails."""

    target_t: DeserializableType
    msg: str
    cause: Optional[exception_formatter.Cause[Exception]] = None
    display_strategy: ErrorDisplayStrategy = ErrorDisplayStrategy.DEFAULT

    @final
    @staticmethod
    def cannot_create_msg(deserializer_desc: str) -> str:
        """Format the message for standard deserializer creation failure."""
        return "cannot create {} deserializer".format(deserializer_desc)

    @final
    def __str__(self) -> str:
        """Format the exception message."""

        def get_metadata(
            e: Exception,
        ) -> exception_formatter.ExceptionData[Exception, Exception]:
            if isinstance(e, DeserializerFactoryError):
                return exception_formatter.ExceptionData(
                    e,
                    e.cause if e.cause is not None else {},
                    e.msg,
                    e.display_strategy,
                )
            return exception_formatter.ExceptionData(
                e, {}, str(e), ErrorDisplayStrategy.DEFAULT
            )

        return exception_formatter.format_exception(cast(Exception, self), get_metadata)


class InternalDeserializerFactoryError(DeserializerFactoryError):
    """Raised when deserializer creation fails. Caught internally."""
