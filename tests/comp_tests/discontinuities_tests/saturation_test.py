import pytest
from pyrunner.components import Constant
from pyrunner.components import BlockDiagram
from pyrunner.components.discontinuities.saturation import Saturation

MAIN_SYS = BlockDiagram("main_sys", "seq")
const = Constant(MAIN_SYS, value=[2, 43, 232, 12321, -1123, 222])


def test_normal_saturation():
    Saturator = Saturation(MAIN_SYS, low_lim=0, up_lim=100)
    Saturator.inputs.update({"value": const})
    MAIN_SYS.build()  # Build code to generate the strings
    print(Saturator.code_str["Execution"])
    MAIN_SYS.remove_components(Saturator)  # Tear down test components


def test_saturation_errors():
    with pytest.raises(AttributeError):
        # Testing for lower_limit and upper_limit error: Both cannot be none.
        Saturator1 = Saturation(MAIN_SYS, low_lim=None, up_lim=None)
        Saturator1.inputs.update({"value": const})
        MAIN_SYS.build(create_code=False)
