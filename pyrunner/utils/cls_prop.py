"""
This module contains a data descriptor that mimics the property behavior for
class attributes. One can use this in the same manner one would use "property".

The classes in this module are based on the following sources:

    [1] Pure Python implementation of the property class:
        https://docs.python.org/3/howto/descriptor.html#properties

    [2] How to make a class property?:
        https://stackoverflow.com/questions/5189699/how-to-make-a-class-property

    [3] Overall structure was based on the abc module:
        https://github.com/python/cpython/blob/master/Lib/abc.py
"""

from inspect import isclass


class classproperty:
    """Data descriptor that mimics "property" objects for class attributes.

    This was done since Python versions earlier than 3.9 can't chain "property"
    and "classmethod" objects to achieve the same effect as what this class
    does. Noting this fget, fset, and fdel cannot be staticmethods. They need
    to be either a normal or a class method. Furthermore, when either of these
    is set they are turned into classmethods and these are not directly callable,
    so to actually access them the __get__ method is used to pass the values to
    the method stored in the classmethod object.
    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):

        self._fget = self._convert_to_classmethod(fget)
        self._fset = self._convert_to_classmethod(fset)
        self._fdel = self._convert_to_classmethod(fdel)
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    @staticmethod
    def persistent(name, value, doc=None):
        """Constructor that returns an immutable classproperty."""

        # Generate classproperty's fget, fset, and fdel

        def read_only_setter(*args):  # This prevents  user from changing the value
            raise AttributeError(f'Class attribute "{name}" cannot change its value')

        def constant_getter(_):  # This will always get a constant value
            return value

        def read_only_deleter(_):  # This prevents a user from deleting the value
            raise AttributeError(f'Class attribute "{name}" cannot be deleted')

        # Define classproperty object

        const_cls_prop = classproperty(constant_getter, read_only_setter, read_only_deleter, doc)
        const_cls_prop.name = name  # Set property name

        # Define protocol blocker to prevent user from directly changing the accessor decorators

        def _create_protocol_block(protocol_name):

            def blocker(*args):
                raise AttributeError(f"Cannot modify class attribute's {protocol_name}")

            return blocker

        # Restrict user from changing classproperty's fget, fset, and fdel

        const_cls_prop.getter = _create_protocol_block("getter")
        const_cls_prop.setter = _create_protocol_block("setter")
        const_cls_prop.deleter = _create_protocol_block("deleter")

        return const_cls_prop

    def __get__(self, obj, cls=None):

        if self._fget is None:  # Verify if getter was set
            raise AttributeError(f'No getter method has been set for classproperty "{self.name}"')
        if cls is None:
            cls = type(obj)
        return self._fget.__get__(obj, cls)()

    def __set__(self, obj, value):

        if self._fset is None:  # Verify if setter was set
            raise AttributeError(f'No setter method has been set for classproperty "{self.name}"')
        obj, cls = self._get_function_arguments(obj)
        return self._fset.__get__(obj, cls)(value)

    def __delete__(self, obj):

        if self._fdel is None:  # Verify if deleter was set
            raise AttributeError(f'No deleter method has been set for classproperty "{self.name}"')
        obj, cls = self._get_function_arguments(obj)
        self._fdel.__get__(obj, cls)()

    def __set_name__(self, obj, name):

        self.name = name

    def setter(self, fset=None):
        """Descriptor to change the setter on a classproperty"""

        self._fset = self._convert_to_classmethod(fset)
        return self

    def getter(self, fget=None):
        """Descriptor to change the getter on a classproperty"""

        self._fget = self._convert_to_classmethod(fget)
        return self

    def deleter(self, fdel=None):
        """Descriptor to change the deleter on a classproperty"""

        self._fdel = self._convert_to_classmethod(fdel)
        return self

    @staticmethod
    def _convert_to_classmethod(func):

        if func is not None:
            if isinstance(func, staticmethod):
                raise TypeError(f"{func.__func__.__name__} cannot be a staticmethod")
            if isinstance(func, classmethod):
                return func
            return classmethod(func)
        return

    @staticmethod
    def _get_function_arguments(obj):

        if isclass(obj):
            return None, obj
        return obj, type(obj)


class CPEnabledMeta(type):
    """
    A metaclass to ensure classproperty objects work as intended when used with
    the class itself.

    This metaclass does two things:

        [1] It prevents the classproperty object from been overwritten by the
            new assigned value when called by the class.

        [2] It gives access to the __delete__ method when calling a classproperty
            object with the class before deleting the attribute itself.

    This is needed if you want to use the classproperty class, so you will have
    to put this as your metaclass if needed.
    """

    def __setattr__(cls, name, value):

        if name in cls.__dict__:
            obj = cls.__dict__.get(name)
            if isinstance(obj, classproperty):
                return obj.__set__(cls, value)  # Access classproperty and return this instead to prevent overwriting it
        return super().__setattr__(name, value)  # Set up attribute normally if not classproperty object

    def __delattr__(cls, name):

        if name in cls.__dict__:
            obj = cls.__dict__.get(name)
            if isinstance(obj, classproperty):
                obj.__delete__(cls)  # Access the __delete__ method for the classproperty object
        super().__delattr__(name)  # Proceed to delete class attribute


class CPEnabled(metaclass=CPEnabledMeta):
    """
    A helper class for CPMeta that enables class properties by inheriting from
    this class directly.
    """

    __slots__ = ()


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
