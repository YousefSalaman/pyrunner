from pyrunner.components import Constant
from pyrunner.components import BlockDiagram
from pyrunner.components.math_op.sqrt import Sqrt

MAIN_SYS = BlockDiagram("main_sys", "seq")
const=Constant(MAIN_SYS,value=[4,25,16,49])
const1=Constant(MAIN_SYS,value=5000)
const2=Constant(MAIN_SYS,value=49)


def test_sqrt():
    sqrt = Sqrt(MAIN_SYS,type="sine")
    sqrt1 = Sqrt(MAIN_SYS,type="square")
    sqrt2 = Sqrt(MAIN_SYS,type="reciprocal")
    sqrt.inputs.update({"value":const})
    sqrt1.inputs.update({"value":const1})
    sqrt2.inputs.update({"value":const2})
    MAIN_SYS.build()  # Build code to generate the strings
    print(sqrt.code_str["Execution"])  # Should be "add = const-const_1+const_2"
    print(sqrt1.code_str["Execution"])  # Should be "add = const-const_1+const_2"
    print(sqrt2.code_str["Execution"])  # Should be "add = const-const_1+const_2"
    MAIN_SYS.remove_components(sqrt,sqrt1,sqrt2)  # Tear down test components
