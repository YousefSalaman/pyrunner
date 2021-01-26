"""
This module extends the standard library's abc module's functionality by
verifying abstractmethods have been overridden with the same type as in the
ABC. The classes in this module can be used in the same manner as the Python's
abc module.

This should work fine classmethods, staticmethods, properties, or any other
built-in class in the Python repository. For custom classes like classproperty,
you'll have to add a decorator like, for example, abstractclassmethod to make
this functionality work correctly.

The ABCMeta metaclass was used to build the metaclass TypeABCMeta to detect
type consistency at class creation, so it gurantees the user overrides the
method. The new metaclass was mixed in with the classproperty metaclass,
CPEnabledMeta, to fuse both features together in case someone wants to use both
at the same time.

The classes on this module are based on the following source:

    [1] Overall structure was based on the abc module:
        https://github.com/python/cpython/blob/master/Lib/abc.py
"""

from inspect import isabstract
from abc import ABCMeta, abstractmethod  # Don't remove abstractmethod
from Simupynk.utils.cls_prop import CPEnabledMeta, classproperty


def _findABCFromBases(bases):

    for base_cls in bases:
        if isabstract(base_cls):
            return base_cls
    return None


def _verifyTypeOverride(cls, abs_cls):

    for abs_method_name in abs_cls.__abstractmethods__:
        method = cls.__dict__.get(abs_method_name)
        abs_method = abs_cls.__dict__[abs_method_name]
        if method is not None:
            _checkTypeConsistency(method, abs_method)


def _checkTypeConsistency(method, abs_method):

    method_type = type(method)
    abs_method_type = type(abs_method)

    # This verification is for built-in python classes
    if method_type is not abs_method_type and method_type is not classproperty:
        if hasattr(abs_method, "__func__"):  # Case for method classes
            raise TypeError('"{}" must be of type "{}"'.format(abs_method.__func__.__name__, type(abs_method).__name__))
        raise TypeError('One of the overridden methods does not match the original type of its respective ABC')

    # This one is for the custom classproperty class since their classes don't match
    if abs_method_type is abstractclassproperty and method_type is not classproperty:
        raise TypeError('One of the overridden methods does not match the original type of its respective ABC')


class abstractclassproperty(classproperty):
    """
    A decorator indicating abstract classproperties.

    It's a direct copy of the depracated "abstractproperty" class from the abc
    module. This has to be implemented to make the classproperty class work for
    ABCs. In other words, do not chain classproperty and abstract property
    since that won't yield the desired result.

    For usage of this class, look at the test scripts for this class.
    """

    __isabstractmethod__ = True


class TypeABCMeta(ABCMeta):
    """
    A metaclass to verify ABCs and their direct child classes have the same
    types when overridden. It does this when a new class is created, so it
    prevents the user from using the abstractmethod unless they have overridden
    the abstractmethod with the correct class.
    """

    def __new__(mcls, name, bases, namespace, **kwargs):

        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        abs_cls = _findABCFromBases(bases)  # The ABC that contains the relevant abstract methods
        if abs_cls is not None:
            _verifyTypeOverride(cls, abs_cls)
        return cls


class TypeABC(metaclass=TypeABCMeta):
    """
    A helper class for the TypeABCMeta metaclass. It enables ABCs that verify
    if its child classes have overridden the abstractmethods with methods that
    have the correct type just by inheriting from this class.
    """

    __slots__ = ()


class CPEnabledTypeABCMeta(CPEnabledMeta, TypeABCMeta):
    """
    A metaclass that mixes the functionality of using classproperties and type
    checking for ABCs.
    """


class CPEnabledTypeABC(metaclass=CPEnabledTypeABCMeta):
    """
    A helper class for CPEnabledTypeABCMeta that enables using classproperties
    and type checking for ABCs just by inhereting from this class directly.
    """

    __slots__ = ()
