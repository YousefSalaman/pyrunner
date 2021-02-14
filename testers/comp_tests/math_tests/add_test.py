from Simupynk.components import *


if __name__ == "__main__":

    main_sys = systems.BlockDiagram("main_sys", "seq")

    const_1 = sources.Constant(main_sys)
    const_2 = sources.Constant(main_sys)

    adder = math_op.Add(main_sys)
    adder.inputs.add(const_1, const_2)
    adder.parameters['comp_signs'] = ['+', '-']

    const_1.parameters.add(value=1)
    const_2.parameters.add(value=3.1415)

    main_sys.build_diagram()

