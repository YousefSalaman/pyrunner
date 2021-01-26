from Simupynk.utils.cls_prop import classproperty, CPEnabled, CPEnabledMeta
from unittest import TestCase
import pytest


class Foo(CPEnabled):  # testing CPEnabled
    _bar = 0

    @classproperty
    @classmethod
    def bar(cls):
        """
        Test class property
        """
        return cls._bar

    @bar.setter
    def bar(cls, value):
        cls._bar = value

    @bar.getter
    def bar(cls):
        return 1

    @bar.deleter
    @classmethod
    def bar(cls):
        print("Deleting...")
        del cls._bar


class FooMeta(metaclass=CPEnabledMeta):  # testing CPEnabledMeta
    _bar = 0

    @classproperty
    @classmethod
    def bar(cls):
        """
        Test class property
        """
        return cls._bar

    @bar.setter
    def bar(cls, value):
        cls._bar = value

    @bar.getter
    def bar(cls):
        return 1

    @bar.deleter
    @classmethod
    def bar(cls):
        print("Deleting...")
        del cls._bar


class TestingFoos(TestCase):

    def test_getter(self):
        object = Foo()
        self.assertEqual(object.bar, 1, "The value of the func should be 1.")

        object = FooMeta()
        self.assertEqual(object.bar, 1, "The value of the func should be 1.")

    def test_setter(self):
        object = Foo()
        object.bar = 1
        self.assertEqual(object.bar, 1, "The expected result is 1")

        Foo.bar = 2
        self.assertEqual(Foo.bar, 1, "The expected result is 1")

        object = FooMeta()
        object.bar = 1
        self.assertEqual(object.bar, 1, "The expected result is 1")
        Foo.bar = 2
        self.assertEqual(Foo.bar, 1, "The expected result is 1")

    def test_del(self):
        # testing switch value error
        with pytest.raises(AttributeError):
            object = Foo()
            del object.bar
            print(Foo._bar)  # It's suppose to give an error since the property is deleted by the deleter
            print(Foo.bar)  # This will also yield an error

            object = FooMeta()
            del object.bar
            print(Foo._bar)  # It's suppose to give an error since the property is deleted by the deleter
            print(Foo.bar)  # This will also yield an error
