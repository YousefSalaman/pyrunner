from pyrunner.components import Constant
from pyrunner.components import BlockDiagram
from pyrunner.components.math_op.divide import Divide

if __name__ == "__main__":
    MAIN_SYS = BlockDiagram("main_sys", "seq")
    const = Constant(MAIN_SYS, value=2)
    const_1 = Constant(MAIN_SYS, value=55)
    divider = Divide(MAIN_SYS)
    divider.inputs.update({"numerator": const})
    divider.inputs.update({"denominator": const_1})
    MAIN_SYS.build()  # Build code to generate the strings
    print(divider.code_str["Execution"])
    MAIN_SYS.remove_components(divider)  # Tear down test components
