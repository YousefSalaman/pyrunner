import pytest

from Simupynk.Simupynk.components import *
from Simupynk.tests.comp_tests.comp_init import InitCompDependent, InitCompInvariant


sys_obj = systems.BlockDiagram("System1", "seq")

a = InitCompDependent(sys_obj)
a_in = InitCompInvariant(sys_obj)
a_in_1 = InitCompDependent(sys_obj)
a_in_2 = InitCompDependent(sys_obj, "dummy_var")
a_out = InitCompInvariant(sys_obj)

b = InitCompInvariant(sys_obj)
b_0 = InitCompInvariant(sys_obj)
b_1 = InitCompDependent(sys_obj)
b_2 = InitCompDependent(sys_obj)

def testing_comps():

    # Order dependent component

    a.inputs["test1"] = a_in_1
    a.inputs["test2"] = a_in_2

    with pytest.raises(TypeError):
        a.verify_properties()  # Will throw TypeError since one of the required inputs are still not assigned

    with pytest.raises(KeyError):
        a.inputs["test4"] = a_in_1  # Will result in KeyError because "test4" is not a key in inputs

    with pytest.raises(TypeError):
        a.inputs["test2"] = 1  # Will result in TypeError since "1" is not a component

    a.inputs.add(test=a_in)  # Assign last required property for inputs

    a.inputs.add(a_in)  # Wont affect anything

    # Note that running a.verify_properties() will still result in the TypeError since
    # the method verifies each of the properties of that object

    with pytest.raises(KeyError):
        a.outputs["result3"] = a_out  # Will result in KeyError because outputs does not accept entries

    a_para = 1.23456789
    a_para_1 = 42

    with pytest.raises(TypeError):
        a.verify_properties()  # Will throw TypeError since one of the required outputs are still not assigned

    a.parameters.update(para=a_para, para1=a_para_1)

    a.verify_properties()  # Nothing will happen since all required properties were filled with a value

    # All of the commented lines below will result in an AttributeError since they are attempting to delete an item of
    # an order-dependent property (inputs)

    # del a.inputs['test1']
    # a.inputs.pop('test')
    # a.inputs.popitem()
    # a.inputs.clear_diagram()

    print(a.inputs, a.outputs, a.parameters)

    # Order-invariant component

    assert b.inputs == {}, "Expected result is {}"
    assert b.outputs == {}, "Expected result is {}"
    assert b.parameters == {}, "Expected result is {}"

    with pytest.raises(KeyError):
        b.parameters[
            "incorrect_key"] = 4  # Will result in KeyError because "incorrect_key" does not conform with the generated key format

    b.inputs.add(b_0, b_1, b_2)
    b.outputs.add(b_1)
    b.parameters.add(3.1415, 42)

    print(b.inputs)
    b.inputs.pop('input_1')
    print(b.inputs)

    print(b.inputs, b.outputs, b.parameters)


def test_order_invariant_component_properties():

    pass


def test_order_dependent_component_properties():

    pass

