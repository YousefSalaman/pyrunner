from abc import abstractmethod
from Simupynk.utils.cls_prop import classproperty
from Simupynk.utils.type_abc import CPEnabledTypeABCMeta, CPEnabledTypeABC, abstractclassproperty
from unittest import TestCase
import pytest


class BarMeta(metaclass=CPEnabledTypeABCMeta):
    _foo = 0
    _bar = 1

    def __init__(self):
        self._bee = 3

    @classmethod
    @abstractmethod
    def foo(cls):
        pass

    @abstractclassproperty
    def bar(cls):
        pass

    @staticmethod
    @abstractmethod
    def fab():
        pass

    @property
    @abstractmethod
    def bee(self):
        pass


class Bar(CPEnabledTypeABC):
    _foo = 0
    _bar = 1

    def __init__(self):
        self._bee = 3

    @classmethod
    @abstractmethod
    def foo(cls):
        pass

    @abstractclassproperty
    def bar(cls):
        pass

    @staticmethod
    @abstractmethod
    def fab():
        pass

    @property
    @abstractmethod
    def bee(self):
        pass


class ChildBar(Bar):

    @classproperty  # If you remove this method, it should cause an TypeError (intended)
    def bar(cls):
        return cls._bar

    @bar.setter
    def bar(cls, value):
        cls._bar = value

    @classmethod  # If you remove this method, it should cause an TypeError (intended)
    def foo(cls):
        return cls._foo

    @staticmethod  # If you remove this method, it should cause an TypeError (intended)
    def fab():
        return 0

    @property  # If you remove this method, it should cause an TypeError (intended)
    def bee(self):
        return self._bee

    @bee.setter
    def bee(self, value):
        print("Set the bee value")
        self._bee = value


class ChildBarMeta(BarMeta):

    @classproperty  # If you remove this method it should cause an TypeError (intended)
    def bar(cls):
        return cls._bar

    @bar.setter
    def bar(cls, value):
        cls._bar = value

    @classmethod  # If you remove this method it should cause an TypeError (intended)
    def foo(cls):
        return cls._foo

    @staticmethod  # If you remove this method it should cause an TypeError (intended)
    def fab():
        return 0

    @property  # If you remove this method it should cause an TypeError (intended)
    def bee(self):
        return self._bee

    @bee.setter
    def bee(self, value):
        print("Set the bee value")
        self._bee = value


class TestingABCs(TestCase):

    def testABC(self):
        a = ChildBar()
        # self.assertEqual(a.foo, 0, "The value should be 0.")
        self.assertEqual(a.bar, 1, "The value should be 1.")
        self.assertEqual(ChildBar.bar, 1, "The value should be 1.")
        # self.assertEqual(a.fab, 0, "The value should be 0.")
        self.assertEqual(a.bee, 3, "The value should be 3.")

        a.bar = 10
        a.bee = 30
        self.assertEqual(a.bar, 10, "The value should be 10.")
        self.assertEqual(a.bee, 30, "The value should be 30.")
        self.assertEqual(ChildBar.bar, 10, "The value should be 10.")

        ChildBar.bar = 2
        self.assertEqual(ChildBar.bar, 2, "The value should be 2.")

        b = ChildBarMeta()
        # self.assertEqual(b.foo, 0, "The value should be 0.")
        self.assertEqual(b.bar, 1, "The value should be 1.")
        self.assertEqual(ChildBarMeta.bar, 1, "The value should be 1.")
        # self.assertEqual(b.fab, 0, "The value should be 0.")
        self.assertEqual(b.bee, 3, "The value should be 3.")

        b.bar = 10
        b.bee = 30
        self.assertEqual(b.bar, 10, "The value should be 10.")
        self.assertEqual(b.bee, 30, "The value should be 30.")
        self.assertEqual(ChildBarMeta.bar, 10, "The value should be 10.")

        ChildBarMeta.bar = 2
        self.assertEqual(ChildBarMeta.bar, 2, "The value should be 2.")

    def testDeletions(self):
        a = ChildBar()
        print(a.bar)
        print(a.foo)
        print(a.fab)
        print(a.bee)

        with pytest.raises(AttributeError):
            del a.bar
            print(a.bar)

            del a.foo
            print(a.foo)

            del a.fab
            print(a.fab)

            del a.bee
            print(a.bee)
