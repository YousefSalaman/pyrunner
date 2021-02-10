import pytest

from Simupynk.components.systems.main_sys import MainSystem
from Simupynk.testers.comp_init import InitCompInvariant, InitCompVariant


def testing_sys():
    sys_obj = MainSystem("System1", "seq")

    a = InitCompVariant(sys_obj)
    assert str(a) == "test_var"
    a_in = InitCompInvariant(sys_obj)
    assert str(a_in) == "test_inv"
    a_in_1 = InitCompVariant(sys_obj)
    assert str(a_in_1) == "test_var_1"
    a_in_2 = InitCompVariant(sys_obj, "dummy_var")
    assert str(a_in_2) == "dummy_var"