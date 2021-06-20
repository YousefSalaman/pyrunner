import pytest

from pyrunner.components import Constant
from pyrunner.components import BlockDiagram
from pyrunner.components.math_op.gain import Gain

MAIN_SYS = BlockDiagram("main_sys", "seq")
const = Constant(MAIN_SYS)
const.parameters.add(value=[2, 43, 232, 12321, -1123, 222])


def test_gain():
    # Creating Gain components:
    gain = Gain(MAIN_SYS, lower_limit=1, upper_limit=400, multiplication="element_wise")
    gain1 = Gain(MAIN_SYS, lower_limit=1, upper_limit=400, multiplication="matrix_mode1")
    gain2 = Gain(MAIN_SYS, lower_limit=1, upper_limit=400, multiplication="matrix_mode2")

    # Adding inputs:
    gain.inputs.update({"value": const})
    gain.inputs.update({"gain": const})
    gain1.inputs.update({"value": const})
    gain1.inputs.update({"gain": const})
    gain2.inputs.update({"value": const})
    gain2.inputs.update({"gain": const})

    # Building system
    MAIN_SYS.build()  # Build code to generate the strings
    MAIN_SYS.remove_components(gain)  # Tear down test components


def test_gain_errors():
    with pytest.raises(AttributeError):
        gain = Gain(MAIN_SYS, lower_limit=None, upper_limit=None, multiplication="element_wise")
        gain.inputs.update({"value": const})
        gain.inputs.update({"gain": const})
        MAIN_SYS.build(create_code=False)

