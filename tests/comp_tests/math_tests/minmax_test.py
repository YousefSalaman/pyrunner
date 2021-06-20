import pytest
from pyrunner.components import Constant
from pyrunner.components import BlockDiagram
from pyrunner.components.math_op.minmax import MinMax

MAIN_SYS = BlockDiagram("main_sys", "seq")
const = Constant(MAIN_SYS, value=[2, 43, 232, 12321, -1123, 222])


def test_min_max():
    min_ = MinMax(MAIN_SYS, type=min)
    max_ = MinMax(MAIN_SYS, type=max)
    min_.inputs.update({"value": const})
    max_.inputs.update({"value": const})
    MAIN_SYS.build()  # Build code to generate the strings
    print(min_.code_str["Execution"])
    print(max_.code_str["Execution"])
    MAIN_SYS.remove_components(min_, max_)  # Tear down test components


def test_minmax_errors():
    with pytest.raises(TypeError):
        # Testing for type parameter error: Cannot be none.
        min1_ = MinMax(MAIN_SYS, type=None)
        min1_.inputs.update({"value": const})
        MAIN_SYS.build(create_code=False)
