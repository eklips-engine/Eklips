## Import libraries & components
import json, pyglet as pg
import os, sys
from classes.locals    import *
from .errors           import *
from typing_extensions import *

## Classes
class NodeMixin:
    separator = "/"

    @property
    def parent(self):
        """The parent of the Node."""
        if hasattr(self, "_NodeMixin__parent"):
            return self.__parent
        return None
    @parent.setter
    def parent(self, value):
        if value is not None and not isinstance(value, (NodeMixin)):
            msg = f"Parent node {value!r} is not of type 'Node'."
            raise TreeError(msg)
        if hasattr(self, "_NodeMixin__parent"):
            parent = self.__parent
        else:
            parent = None
        if parent is not value:
            self.__check_loop(value)
            self.__detach(parent)
            self.__attach(value)

    def __check_loop(self, node):
        if node is not None:
            if node is self:
                msg = "Cannot set parent. %r cannot be parent of itself."
                raise LoopError(msg % (self,))
            if any(child is self for child in node.iter_path_reverse()):
                msg = "Cannot set parent. %r is parent of %r."
                raise LoopError(msg % (self, node))
    def __detach(self, parent):
        # pylint: disable=W0212,W0238
        if parent is not None:
            parentchildren = parent.__children_or_empty
            if ASSERTIONS:  # pragma: no branch
                assert any(child is self for child in parentchildren), "Tree is corrupt."  # pragma: no cover
            # ATOMIC START
            parent.__children = [child for child in parentchildren if child is not self]
            self.__parent = None
            # ATOMIC END
    def __attach(self, parent):
        # pylint: disable=W0212
        if parent is not None:
            parentchildren = parent.__children_or_empty
            if ASSERTIONS:  # pragma: no branch
                assert not any(child is self for child in parentchildren), "Tree is corrupt."  # pragma: no cover
            # ATOMIC START
            parentchildren.append(self)
            self.__parent = parent
            # ATOMIC END

    @property
    def __children_or_empty(self):
        if not hasattr(self, "_NodeMixin__children"):
            self.__children = []
        return self.__children
    @property
    def children(self):
        """The children of this node."""
        return tuple(self.__children_or_empty)
    @staticmethod
    def __check_children(children):
        seen = set()
        for child in children:
            if not isinstance(child, (NodeMixin)):
                msg = f"Cannot add non-node object {child!r}. It is not a subclass of 'Node'."
                raise TreeError(msg)
            childid = id(child)
            if childid not in seen:
                seen.add(childid)
            else:
                msg = f"Cannot add node {child!r} multiple times as child."
                raise TreeError(msg)
    @children.setter
    def children(self, children):
        # convert iterable to tuple
        children = tuple(children)
        NodeMixin.__check_children(children)
        # ATOMIC start
        old_children = self.children
        del self.children
        try:
            for child in children:
                child.parent = self
            if ASSERTIONS:  # pragma: no branch
                assert len(self.children) == len(children)
        except Exception:
            self.children = old_children
            raise
        # ATOMIC end
    @children.deleter
    def children(self):
        children = self.children
        for child in self.children:
            child.parent = None
        if ASSERTIONS:  # pragma: no branch
            assert len(self.children) == 0

    @property
    def path(self):
        """The path of the Node."""
        return self._path
    @property
    def _path(self):
        return tuple(reversed(list(self.iter_path_reverse())))

    def iter_path_reverse(self):
        """Iterate up the tree from the current node to the root node."""
        node = self
        while node is not None:
            yield node
            node = node.parent