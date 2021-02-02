
import pytest
from unittest import TestCase
import Simupynk.components as comps


INPUT_INFO = (
    {"test", "test1", "test2"},  # Required inputs properties
    {"test", "test1", "test2", "test3"}  # All input properties
)

OUTPUT_INFO = (
    {"result", "result1"},  # Required outputs properties
    {"result", "result1", "result2"}  # All output properties
)

PARAMETER_INFO = (
    {"para", "para1"},  # Required parameters
    {"para", "para1", "para2"}  # All parameters
)


class InitCompVariant(comps.BaseComponent):

    has_init_cond = comps.generateHasInitCond(True)

    input_info = comps.generateInputInfo(INPUT_INFO)

    output_info = comps.generateOutputInfo(OUTPUT_INFO)

    parameter_info = comps.generateParameterInfo(PARAMETER_INFO)

    default_name = comps.generateDefaultName("test")

    def generateComponentString(self):

        print("Just a test")
        super().generateComponentString()


class InitCompInvariant(comps.BaseComponent):

    has_init_cond = comps.generateHasInitCond(True)

    input_info = comps.generateInputInfo(None)

    output_info = comps.generateOutputInfo(None)

    parameter_info = comps.generateParameterInfo(None)

    default_name = comps.generateDefaultName("test")

    def generateComponentString(self):

        print("Just a test")
        super().generateComponentString()

def testingComps():
    ## Order variant component

    a = InitCompVariant()

    a_in = InitCompInvariant()
    a_in_1 = InitCompVariant()
    a_in_2 = InitCompVariant()

    a.inputs["test1"] = a_in_1
    a.inputs["test2"] = a_in_2
    with pytest.raises(TypeError):
        a._verifyRequiredComponentProperties()  # Will throw TypeError since one of the required properties was not assigned a component

    a.inputs["test"] = a_in  # Assign last required property for inputs

    # Note that running a._verifyRequiredComponentProperties() will still result in the TypeError since
    # the method verifies each of the properties of that object
    a_out = InitCompInvariant()
    a_out_1 = InitCompVariant()
    a_out_2 = "Just a test"

    with pytest.raises(KeyError):
        a.outputs["result3"] = a_out  # Will result in KeyError because no it's not part of the existing properties

    with pytest.raises(TypeError):
        a.outputs["result"] = a_out_2  # Will result in TypeError since a_out_2 is not a component or numeric

    a.outputs["result"] = a_out
    a.outputs["result1"] = a_out_1

    a_para = InitCompInvariant()
    a_para_1 = InitCompVariant()

    a.parameters.update(para=a_out, para1=a_out_1)

    a.verifyComponentProperties()  # Nothing will happen since all required properties were filled with a value

    print(a.inputs, a.outputs, a.parameters)

    ## Order-invariant component

    b = InitCompInvariant()
    assert b.inputs == {}, "Expected result is {}"
    assert b.outputs == {}, "Expected result is {}"
    assert b.parameters == {}, "Expected result is {}"

    with pytest.raises(KeyError):
        b.inputs["incorrect_key"] = 4  # Will result in KeyError because "incorrect_key" does not conform with the generated key format

    b_0 = InitCompInvariant()
    b_1 = InitCompVariant()
    b_2 = InitCompVariant()

    b.inputs.update(b_0, b_1, b_2, 3.1415, 42)
    b.outputs.update(b_1, 42)
    b.parameters.update(b_2, 3.1415, 42)
    b.outputs["output_1"] = 3.1415  # You can change/add components if the key conforms to the generated key format

    print(b.inputs, b.outputs, b.parameters)

