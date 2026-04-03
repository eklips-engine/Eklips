## Import libraries & components
from typing            import *
from classes.locals    import *
from typing_extensions import *

## Classes
@disjoint_base
class _export:
    def __init__(self, type_=None, default=None, hint=None, fget=None, fset=None):
        self.type    = type_
        self.default = default
        self.hint    = hint
        self.fget    = fget
        self.fset    = fset

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.fget:
            return self.fget(instance)
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value):
        if self.fset:
            return self.fset(instance, value)
        instance.__dict__[self.name] = value

    def getter(self, fget):
        self.fget = fget
        return self

    def setter(self, fset):
        self.fset = fset
        return self

## Expot function
def export(default=None, type_=None, hint=None):
    """
    Use this class to expose a value as a property in the editor.
    This class is similar to the `property` class in Python.
    
    "Wait a sec, this isn't a class!" You might be saying, well,
    this is a decorator to make the `_export` class, and do you
    really wanna type in `export.set_metadata(..)` every time you
    wanna make an export property instead of just `@export(..)`?
    
    Args:
        default: The default value to use.
        type: The name of the type that the value should be (int, str, list, bool...)
        hint: How to display this property in the editor
    
    Hints:
        int:                  An integer
        float:                A float.
        str:                  A string.
        int/float, float/int: A float or integer.
        file_path/type:       A filepath of type `type`.
        color:                An RGBA color.
        slider:               A number but displayed as a slider instead of a textentry.
        font:                 A font name.
        bool:                 As a Checkbox.
        time:                 A span of time in seconds.
        file_paths/type:      A list of filepaths of type `type`.
        vector2/ab:           A 2D Vector with the values A and B.
        transform:            A Transform object.
        windowid:             The ID of a Window. Will be displayed as a dropdown of WIDs.
        viewportid:           The ID of a Viewport. Will be displayed as a dropdown of VIDs.
        batchid:              The ID of a Batch. Will be displayed as a dropdown of BIDs.
    """
    def wrapper(func):
        return _export(
            fget    = func,
            default = default,
            type_   = type_,
            hint    = hint,
        )
    return wrapper

## Meta class
class _exportmeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # Start with parent's properties
        props = {}
        for base in reversed(bases):
            if hasattr(base, "_properties"):
                props.update(base._properties)

        # Add properties in this class
        for key, value in namespace.items():
            if isinstance(value, _export):
                props[key] = {
                    "default": value.default,
                    "type": value.type,
                    "hint": value.hint,
                    "getter": value.fget,
                    "setter": value.fset
                }

        cls._properties = props
        return cls