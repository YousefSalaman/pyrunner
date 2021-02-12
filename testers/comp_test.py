import pytest

from Simupynk.testers.comp_init import InitCompInvariant
from Simupynk.testers.comp_init import InitCompVariant
from Simupynk.components.systems.diagram import BlockDiagram


def testing_comps():
    ## Order variant component

    sys_obj = BlockDiagram("System1", "seq")

    a = InitCompVariant(sys_obj)
    a_in = InitCompInvariant(sys_obj)
    a_in_1 = InitCompVariant(sys_obj)
    a_in_2 = InitCompVariant(sys_obj, "dummy_var")

    a.inputs["test1"] = a_in_1
    a.inputs["test2"] = a_in_2
    with pytest.raises(TypeError):
        a.verify_component_properties()  # Will throw TypeError since one of the required properties was not assigned a component

    a.inputs["test"] = a_in  # Assign last required property for inputs

    # Note that running a.verify_component_properties() will still result in the TypeError since
    # the method verifies each of the properties of that object
    a_out = InitCompInvariant(sys_obj)
    a_out_1 = InitCompVariant(sys_obj)
    a_out_2 = "Just a test"

    with pytest.raises(KeyError):
        a.outputs["result3"] = a_out  # Will result in KeyError because no it's not part of the existing properties

    with pytest.raises(TypeError):
        a.outputs["result"] = a_out_2  # Will result in TypeError since a_out_2 is not a component or numeric

    a.outputs["result"] = a_out
    a.outputs["result1"] = a_out_1

    a_para = 1.23456789
    a_para_1 = 42

    a.parameters.update(para=a_para, para1=a_para_1)

    a.verify_component_properties()  # Nothing will happen since all required properties were filled with a value

    print(a.inputs, a.outputs, a.parameters)

    ## Order-invariant component

    b = InitCompInvariant(sys_obj)
    assert b.inputs == {}, "Expected result is {}"
    assert b.outputs == {}, "Expected result is {}"
    assert b.parameters == {}, "Expected result is {}"

    with pytest.raises(KeyError):
        b.parameters[
            "incorrect_key"] = 4  # Will result in KeyError because "incorrect_key" does not conform with the generated key format

    b_0 = InitCompInvariant(sys_obj)
    b_1 = InitCompVariant(sys_obj)
    b_2 = InitCompVariant(sys_obj)

    b.inputs.update(b_0, b_1, b_2, "3.1415", "testing")
    b.outputs.update(b_1, 42)
    b.parameters.update(3.1415, 42)
    b.outputs["output_1"] = 3  # You can change/add components if the key conforms to the generated key format

    print(b.inputs, b.outputs, b.parameters)