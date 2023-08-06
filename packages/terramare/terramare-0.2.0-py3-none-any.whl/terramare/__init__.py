"""Automatically deserialize complex objects from simple Python types."""

from .errors import DeserializationError, DeserializerFactoryError  # noqa: F401
from .terramare import (  # noqa: F401
    create_deserializer,
    create_deserializer_factory,
    deserialize_into,
)
