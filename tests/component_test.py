
import Simupynk.components as comps
from unittest import TestCase
import pytest


class InitComp(comps.BaseComponent):

    has_init_cond = comps.HAS_INIT_COND_TRUE

    input_lim = comps.generateInputLim((1, 3))  # Input ranges from 1 to 3

    default_name = comps.generateDefaultName("test")

    def generateComponentString(self):

        print("Just a test")
        super().generateComponentString()

class TestBaseComponent(TestCase):
    def test_verify_input_size(self):
        a = InitComp(inputs=[])
        b = InitComp(inputs=[0, 1, 2, 3])  # Should give you an Attribute error for range error
        with pytest.raises(AttributeError):
            a.verifyInputSize()
            b.verifyInputSize()
