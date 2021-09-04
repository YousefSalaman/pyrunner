from pyrunner.components import *

MAIN_SYS = systems.BlockDiagram("main_sys", "seq")

# create comps

const = sources.Constant(MAIN_SYS, value=15)
const_1 = sources.Constant(MAIN_SYS, value='np.array([9, 5, 6, 15, 2])')


def array_difference_test():

    differ = math_op.Difference(MAIN_SYS, init_cond=4)
    differ.inputs.update({"value": const_1})
    MAIN_SYS.outputs.add(differ)
    MAIN_SYS.build(create_code=False)
    print(differ.code_str["Execution"])
    MAIN_SYS.remove_components(differ)


def int_difference_test():

    differ = math_op.Difference(MAIN_SYS, init_cond=2)
    differ.inputs.update({"value": const})
    MAIN_SYS.outputs.add(differ)
    MAIN_SYS.build(create_code=False)
    print(differ.code_str["Execution"])
    MAIN_SYS.remove_components(differ)
