"""Utilities for formatting nested terramare exceptions."""

from typing import (
    Callable,
    Generic,
    List,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)

import attr

E = TypeVar("E", bound=Exception)
K = TypeVar("K")


Cause = Union[E, Mapping[str, E]]


@attr.s(auto_attribs=True, frozen=True)
class ExceptionData(Generic[K, E]):
    """
    Interface for tree formatted exceptions.

    :var key: Key used for determining exception uniqueness. An exception's
        details will only be displayed once even if it occurs multiple times.
    :var cause: Cause of the exception, either another exception or a labelled
        collection of exceptions.
    :var msg: Exception message.
    :var always_display_msg: If set, the exception's message will always be
        displayed, even if it could be collapsed because either:

        - Its cause is a single exception;
        - It is part of a collection of labelled exceptions.
    """

    key: K
    cause: Cause[E]
    msg: str
    always_display_msg: bool


def format_exception(
    exception: E, get_metadata: Callable[[E], ExceptionData[K, E]]
) -> str:
    """Recursively format a tree of exceptions."""

    def get_tree_(
        root: E, prefix: Optional[str] = None, is_root: bool = False
    ) -> _Tree[_Elt[K]]:
        """Convert an exception to a tree of messages."""

        metadata = get_metadata(root)

        def get_msg(is_leaf: bool) -> str:
            if prefix is None:
                return metadata.msg
            if metadata.always_display_msg or is_leaf or is_root:
                # Always display the message of a leaf or the root, as otherwise
                # the exception doesn't make much sense.
                return f"{prefix}: {metadata.msg}"
            return prefix

        if isinstance(metadata.cause, Exception):
            child = cast(E, metadata.cause)
            if metadata.always_display_msg or is_root:
                return _Tree(_Elt(metadata.key, get_msg(False)), [get_tree_(child)])
            # If an exception is caused by a single other exception, and the
            # message doesn't need to be displayed, don't include that exception
            # in the tree at all. Instead, replace it by its cause.
            return get_tree_(child, prefix)
        else:
            children = cast(Mapping[str, E], metadata.cause)
            return _Tree(
                _Elt(metadata.key, get_msg(len(children) == 0)),
                [get_tree_(child, f"[{key}]") for key, child in children.items()],
            )

    return _format_exception_tree(get_tree_(exception, is_root=True))


@attr.s(auto_attribs=True, frozen=True)
class _Elt(Generic[K]):
    key: K
    msg: str


T = TypeVar("T")


@attr.s(auto_attribs=True, frozen=True)
class _Tree(Generic[T]):
    element: T
    children: List["_Tree[T]"]


def _format_exception_tree(root: _Tree[_Elt[K]], max_width: int = 100) -> str:
    seen: List[Tuple[str, K]] = []
    return _format_exception_tree_recursive(root, seen, max_width=max_width, depth=0)


def _format_exception_tree_recursive(
    root: _Tree[_Elt[K]], seen: List[Tuple[str, K]], max_width: int, depth: int
) -> str:
    def inner(seen: List[Tuple[str, K]]) -> str:
        if not root.children:
            return root.element.msg
        if len(root.children) == 1 and not root.children[0].children:
            # If there's only a single child, and it has no children itself,
            # display this element and its child on a single line.
            rv = root.element.msg + ": " + root.children[0].element.msg
            if 2 * depth + len(rv) <= max_width:
                # Provided the line is not too long!
                return rv
        return "\n".join(
            [root.element.msg + ":"]
            + [
                child_str
                for child_str in [
                    _indent(
                        _format_exception_tree_recursive(
                            root=child, seen=seen, max_width=max_width, depth=depth + 1
                        ),
                        "- ",
                        "  ",
                    )
                    for child in root.children
                ]
            ]
        )

    root_str = inner([])
    if (root_str, root.element.key) in seen:
        # If this exception has already been seen in the tree, don't display
        # it in full detail - just refer to the previous occurence.
        return f"{root.element.msg} as above"
    root_str = inner(seen)
    seen.append((root_str, root.element.key))
    return root_str


def _indent(s: str, head_prefix: str, tail_prefix: str) -> str:
    return "\n".join(
        [
            (head_prefix if lineno == 0 else tail_prefix) + line
            for lineno, line in enumerate(s.splitlines())
        ]
    )
