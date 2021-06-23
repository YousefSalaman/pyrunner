from pyrunner.components import Constant
from pyrunner.components import BlockDiagram
from pyrunner.components.math_op.product import Product

MAIN_SYS = BlockDiagram("main_sys", "seq")
const = Constant(MAIN_SYS, value=100)
const1 = Constant(MAIN_SYS, value=10)
const2 = Constant(MAIN_SYS, value=15)
const3 = Constant(MAIN_SYS, value=300)


def test_product():
    # Creating products
    mult = Product(MAIN_SYS, mult="element")
    mult2 = Product(MAIN_SYS, mult="matrix1")
    mult3 = Product(MAIN_SYS, mult="matrix2")

    # product1
    mult.inputs.update({"value": const})
    mult.inputs.update({"constant": const1})

    # product2
    mult2.inputs.update({"value": const2})
    mult2.inputs.update({"constant": const3})

    # product3
    mult3.inputs.update({"value": const2})
    mult3.inputs.update({"constant": const3})

    MAIN_SYS.build()  # Build code to generate the strings
    # executors.run(MAIN_SYS, ctrl_inputs)
    print(mult.code_str["Execution"])
    print(mult2.code_str["Execution"])
    print(mult3.code_str["Execution"])
    MAIN_SYS.remove_components(mult)  # Tear down test components
