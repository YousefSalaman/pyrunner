
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


class TestBaseComponent(TestCase):
    def test_verify_input_size(self):
        pass
        # a = InitComp(inputs=[])  # Components no longer have the argument "inputs" in constructor
        # b = InitComp(inputs=[0, 1, 2, 3])  # Should give you an Attribute error for range error
        # with pytest.raises(AttributeError):
        #     a.verifyInputSize()  # No longer exists. Use a.verifyComponentProperties() instead
        #     b.verifyInputSize()
