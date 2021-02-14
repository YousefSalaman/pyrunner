from Simupynk.components.systems.diagram import BlockDiagram
from Simupynk.testers.comp_tests.comp_init import InitCompInvariant, InitCompDependent


def testing_sys():
    sys_obj = BlockDiagram("System1", "seq")

    a = InitCompDependent(sys_obj)
    assert str(a) == "test_var"
    a_in = InitCompInvariant(sys_obj)
    assert str(a_in) == "test_inv"
    a_in_1 = InitCompDependent(sys_obj)
    assert str(a_in_1) == "test_var 1"
    a_in_2 = InitCompDependent(sys_obj, "dummy_var")
    assert str(a_in_2) == "dummy_var"