import pytest
from Simupynk.testers.component_init import InitCompSystem, InitCompInvariant, InitCompVariant


def testingSys():

    SystemObj = InitCompSystem("System1")

    a = InitCompVariant(SystemObj)
    assert str(a) == "test_var"
    a_in = InitCompInvariant(SystemObj)
    assert str(a_in) == "test_inv"
    a_in_1 = InitCompVariant(SystemObj)
    assert str(a_in_1) == "test_var_1"
    a_in_2 = InitCompVariant(SystemObj, "dummy_var")
    assert str(a_in_2) == "dummy_var"
