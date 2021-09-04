from pyrunner.components import *

MAIN_SYS = systems.BlockDiagram("main_sys", "seq")

const = sources.Constant(MAIN_SYS, value=8)


def derivative_test():

    derivative = math_op.Derivative(MAIN_SYS, init_cond=5, sample_time=0)
    derivative.inputs.update({"value": const})
    MAIN_SYS.outputs.add(derivative)
    MAIN_SYS.build(create_code=False)
    print(derivative.code_str["Set Up"], derivative.code_str["Execution"])
    MAIN_SYS.remove_components(derivative)
