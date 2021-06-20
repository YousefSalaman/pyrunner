import pytest
from pyrunner.components import Constant
from pyrunner.components import BlockDiagram
from pyrunner.components.discontinuities.saturation import Saturation

MAIN_SYS = BlockDiagram("main_sys", "seq")
const = Constant(MAIN_SYS, value=[2, 43, 232, 12321, -1123, 222])


def test_normal_saturation():
    Saturator = Saturation(MAIN_SYS, lower_limit=0, upper_limit=100, out_min=-10, out_max=1000)
    Saturator.inputs.update({"value": const})
    MAIN_SYS.build()  # Build code to generate the strings
    print(Saturator.code_str["Execution"])
    MAIN_SYS.remove_components(Saturator)  # Tear down test components


def test_saturation_errors():
    with pytest.raises(AttributeError):
        # Testing for lower_limit and upper_limit error: Both cannot be none.
        Saturator1 = Saturation(MAIN_SYS, lower_limit=None, upper_limit=None, out_min=-0, out_max=1000)
        Saturator1.inputs.update({"value": const})

        # Testing error that triggers if out_min is not greater than the lower_limit or the upper_limit
        Saturator2 = Saturation(MAIN_SYS, lower_limit=0, upper_limit=100, out_min=0, out_max=1000)
        Saturator2.inputs.update({"value": const})

        # Testing error that triggers if out_max is not greater than the lower_limit or the upper_limit
        Saturator3 = Saturation(MAIN_SYS, lower_limit=0, upper_limit=1000, out_min=-10, out_max=1000)
        Saturator3.inputs.update({"value": const})
        MAIN_SYS.build(create_code=False)

