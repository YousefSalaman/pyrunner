
import pytest
from Simupynk.testers.component_init import InitCompSystem, InitCompInvariant, InitCompVariant

def testingComps():
    ## Order variant component

    SystemObj = InitCompSystem("System1")

    a = InitCompVariant(SystemObj)
    a_in = InitCompInvariant(SystemObj)
    a_in_1 = InitCompVariant(SystemObj)
    a_in_2 = InitCompVariant(SystemObj , "dummy_var")

    a.inputs["test1"] = a_in_1
    a.inputs["test2"] = a_in_2
    with pytest.raises(TypeError):
        a.verify_component_properties()  # Will throw TypeError since one of the required properties was not assigned a component

    a.inputs["test"] = a_in  # Assign last required property for inputs

    # Note that running a.verify_component_properties() will still result in the TypeError since
    # the method verifies each of the properties of that object
    a_out = InitCompInvariant(SystemObj)
    a_out_1 = InitCompVariant(SystemObj)
    a_out_2 = "Just a test"

    with pytest.raises(KeyError):
        a.outputs["result3"] = a_out  # Will result in KeyError because no it's not part of the existing properties

    with pytest.raises(TypeError):
        a.outputs["result"] = a_out_2  # Will result in TypeError since a_out_2 is not a component or numeric

    a.outputs["result"] = a_out
    a.outputs["result1"] = a_out_1

    a_para = InitCompInvariant(SystemObj)
    a_para_1 = InitCompVariant(SystemObj)

    a.parameters.update(para=a_out, para1=a_out_1)

    a.verify_component_properties()  # Nothing will happen since all required properties were filled with a value

    print(a.inputs, a.outputs, a.parameters)

    ## Order-invariant component

    b = InitCompInvariant(SystemObj)
    assert b.inputs == {}, "Expected result is {}"
    assert b.outputs == {}, "Expected result is {}"
    assert b.parameters == {}, "Expected result is {}"

    with pytest.raises(KeyError):
        b.inputs["incorrect_key"] = 4  # Will result in KeyError because "incorrect_key" does not conform with the generated key format

    b_0 = InitCompInvariant(SystemObj)
    b_1 = InitCompVariant(SystemObj)
    b_2 = InitCompVariant(SystemObj)

    b.inputs.update(b_0, b_1, b_2, 3.1415, 42)
    b.outputs.update(b_1, 42)
    b.parameters.update(b_2, 3.1415, 42)
    b.outputs["output_1"] = 3.1415  # You can change/add components if the key conforms to the generated key format

    print(b.inputs, b.outputs, b.parameters)

