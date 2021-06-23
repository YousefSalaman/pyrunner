from pyrunner.components import Constant
from pyrunner.components import BlockDiagram
from pyrunner.components.math_op.exponent import Exponent

MAIN_SYS = BlockDiagram("main_sys", "seq")
const = Constant(MAIN_SYS, value=[4,25,16,49])
const1 = Constant(MAIN_SYS, value=5000)
const2 = Constant(MAIN_SYS, value=49)


def test_exp():
    exp = Exponent(MAIN_SYS, exp=const2)
    exp1 = Exponent(MAIN_SYS, exp=const2)
    exp.inputs.update({"base":const})
    exp1.inputs.update({"base":const1})
    MAIN_SYS.build()  # Build code to generate the strings
    print(exp.code_str["Execution"])  # Should be "add = const-const_1+const_2"
    print(exp1.code_str["Execution"])  # Should be "add = const-const_1+const_2"
    MAIN_SYS.remove_components(exp, exp1)  # Tear down test components
